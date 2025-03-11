import os
from pathlib import Path
from markdown_to_blocks import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.split("\n"):
        line = line.strip()  # Remove leading/trailing spaces
        if line.startswith("# "):  
            return line[2:].strip()  # Extract title and remove extra spaces
    return ""  # Return empty string if no title found

def generate_page(from_path, template_path, dest_path, basepath="/"):
    """Generates an HTML page from a Markdown file using a template."""
    print(f"Generating page from {from_path} using {template_path} to {dest_path}")

    # Read markdown content
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    # Read template content
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Process markdown
    title = extract_title(markdown) or "Untitled"
    node = markdown_to_html_node(markdown)
    html = node.to_html()

    # Ensure destination directory exists BEFORE writing
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path:
        os.makedirs(dest_dir_path, exist_ok=True)

    # Replace placeholders in template
    page_content = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Fix absolute links (href="/" and src="/") to include basepath
    page_content = page_content.replace('href="/', f'href="{basepath}')
    page_content = page_content.replace('src="/', f'src="{basepath}')

    # Write final HTML to destination
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page_content)

    print(f"Generated page at {dest_path}")



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    """Recursively converts Markdown files to HTML using a template."""
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):  # If it's a file, process it
            dest_path = Path(dest_path).with_suffix(".html")  # Change .md to .html
            generate_page(from_path, template_path, dest_path, basepath)
        elif os.path.isdir(from_path):  # If it's a directory, recurse
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
