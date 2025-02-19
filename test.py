def truncate_text(text):
    if len(text) > 30:
        truncated_text = text[:30]
        truncated_text = truncated_text[:-3] + "..."
        return truncated_text
    else:
        return text

if __name__ == "__main__":
    text1 = "less than 30"
    text2 = "more than 30 characters long and I want to see if it will truncate the text"

    print(truncate_text(text1))
    print(truncate_text(text2))
