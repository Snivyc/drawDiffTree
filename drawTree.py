import os
import sys

assert len(sys.argv) == 3
# print(sys.argv[1], sys.argv[2])
before_filename, after_filename = sys.argv[1:]
print(before_filename, after_filename)
# print("gumtree parse " +before_filename)
p=os.popen("gumtree parse " +before_filename)
json_AST_before = p.read()

p=os.popen("gumtree parse " +after_filename)
json_AST_after = p.read()

p=os.popen("gumtree diff " +before_filename + " " + after_filename)
diffscript = p.read()
print(diffscript)
from main import main
main(json_AST_before,json_AST_after,diffscript)