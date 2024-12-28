import jiwer

print('hello world!')

target = 'hi'
prediction = 'hello'

print(jiwer.cer(target, prediction))
print(jiwer.wer(target, prediction))
