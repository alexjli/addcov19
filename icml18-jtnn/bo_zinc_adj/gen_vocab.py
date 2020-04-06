vocab = set()
with open('samples_vocab.txt') as fp:
    vocab.union((line.strip() for line in fp))
