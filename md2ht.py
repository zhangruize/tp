import markdown
import codecs
import sys

input_file = codecs.open(sys.argv[1], mode="r", encoding="utf-8")
text = input_file.read()
html = markdown.markdown(text, extensions=['extra'])
output_file = codecs.open(sys.argv[2], "w",
                          encoding="utf-8",
                          errors="xmlcharrefreplace"
)
output_file.write(html)