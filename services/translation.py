from transformers import MT5Tokenizer, MT5ForConditionalGeneration


class Translation:
    def __init__(self) -> None:
        self.model_name = "persiannlp/mt5-large-parsinlu-translation_en_fa"
        self.tokenizer = MT5Tokenizer.from_pretrained(self.model_name)
        self.model = MT5ForConditionalGeneration.from_pretrained(self.model_name)

    def translate(self, input_string, **generator_args):
        input_ids = self.tokenizer.encode(input_string, return_tensors="pt")
        res = self.model.generate(input_ids,max_length=512, **generator_args)
        output = self.tokenizer.batch_decode(res, skip_special_tokens=True)
        return output

translation = Translation()

if __name__ == '__main__':
    tr = Translation()
    print(tr.translate('today is a nice day.'))