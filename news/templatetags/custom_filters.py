from django import template

register = template.Library()


@register.filter(name='censor')
def censor(text):
    badwords = ("сука", "блядь", "пизда", "хуй", "ебать", "похуй", "заебись")
    sentence = text.split()

    for index, word in enumerate(sentence):
        if any(badword in word.lower() for badword in badwords):
            sentence[index] = "".join(['*' if c.isalpha() else c for c in word])

    return " ".join(sentence)