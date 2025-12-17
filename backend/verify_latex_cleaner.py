import re

def clean_content(content):
    print(f"Original: {content}")
    # Remove $$ ... $$
    content = re.sub(r'\$\$(.*?)\$\$', r'\1', content, flags=re.DOTALL)
    # Remove \text{...}
    content = re.sub(r'\\text\{(.*?)\}', r'\1', content)
    # Replace \to with ->
    content = content.replace(r'\to', '->')
    # Remove \[ ... \]
    content = re.sub(r'\\\[(.*?)\\\]', r'\1', content, flags=re.DOTALL)
    print(f"Cleaned:  {content}")
    return content

test_str = r"$$\text{A} \to \text{C} \to \text{E}$$"
result = clean_content(test_str)

expected = "A -> C -> E"
if result.strip() == expected:
    print("✅ Logic Correct")
else:
    print("❌ Logic Failed")
