from pandas import DataFrame

print('Copying to clipboard...', end=' ')
df=DataFrame(['Text to copy'])
df.to_clipboard(index=False,header=False)
print('done.')