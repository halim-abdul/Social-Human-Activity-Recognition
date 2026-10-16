"""Optional supervised DistilBERT training. Network/model downloads are explicit."""
from pathlib import Path
from .schema import LABELS

def train_transformer(train, validation, output_dir, checkpoint="distilbert/distilbert-base-uncased",
                      epochs=2, seed=42):
    from datasets import Dataset
    from transformers import (AutoTokenizer, AutoModelForSequenceClassification,
                              TrainingArguments, Trainer, DataCollatorWithPadding, set_seed)
    from sklearn.metrics import f1_score
    from .privacy import redact
    if set(train.subject_id) & set(validation.subject_id):
        raise ValueError("Train and validation subjects overlap")
    set_seed(seed)
    label2id = {label: i for i, label in enumerate(LABELS)}
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    def convert(frame):
        dataset = Dataset.from_dict({
            "text": frame.text.map(redact).tolist(),
            "labels": frame.label.map(label2id).tolist()})
        return dataset.map(lambda batch: tokenizer(batch["text"], truncation=True,
                                                   max_length=256), batched=True,
                           remove_columns=["text"])
    model = AutoModelForSequenceClassification.from_pretrained(
        checkpoint, num_labels=len(LABELS), label2id=label2id,
        id2label={i: label for label, i in label2id.items()})
    arguments = TrainingArguments(
        output_dir=str(output_dir), learning_rate=2e-5, num_train_epochs=epochs,
        per_device_train_batch_size=8, per_device_eval_batch_size=16,
        eval_strategy="epoch", save_strategy="epoch", load_best_model_at_end=True,
        metric_for_best_model="macro_f1", report_to=[], seed=seed,
        data_seed=seed, save_total_limit=2)
    def metrics(result):
        logits, labels = result
        return {"macro_f1": f1_score(labels, logits.argmax(-1), labels=list(range(len(LABELS))),
                                     average="macro", zero_division=0)}
    trainer = Trainer(model=model, args=arguments, train_dataset=convert(train),
                      eval_dataset=convert(validation),
                      data_collator=DataCollatorWithPadding(tokenizer), compute_metrics=metrics)
    trainer.train()
    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))
    return trainer

def predict_transformer(model_dir, texts, threshold=.5):
    from transformers import pipeline
    from .privacy import redact
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must lie in [0,1]")
    if not Path(model_dir).is_dir():
        raise ValueError("Provide a locally trained model directory")
    classifier = pipeline("text-classification", model=str(model_dir), tokenizer=str(model_dir))
    results = classifier([redact(t) for t in texts], truncation=True, max_length=256)
    return [dict(label=r["label"] if r["score"] >= threshold else "abstain",
                 confidence=float(r["score"])) for r in results]
