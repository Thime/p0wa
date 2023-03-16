from transformers import pipeline, set_seed

# configuración del modelo
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B') # Second line
prompt = "The current stock market" # Third line
res = generator(prompt, max_length=50, do_sample=True, temperature=0.9) # Fourth line
print(res[0]['generated_text'])
with open('gpttext.txt', 'w') as f:
    f.writelines(res[0]['generated_text'])
