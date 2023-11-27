import os
import sys
import math

from pprint import pprint
from dataclasses import dataclass

@dataclass
class Token:
	TYPE: str
	VALUE: str
	ARGC: str
	ARGV: str

def prod(a):
	while (len(a) > 1):
		a[0] *= a[1]
		a.pop(1)
	return a[0]

def lex(code):
	code = list((code + "\0").replace("\0", " \0"))
	pos = 0

	buf = ""
	varNames = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
	tokens = []

	while (code[pos] != "\0"):
		if (code[pos] in "0123456789"):
			while (code[pos] in "0123456789"):
				buf += code[pos]
				pos += 1
			tokens.append(Token("intlit", buf, None, None))
			buf = ""
		elif (code[pos] in varNames):
			while (code[pos] in varNames):
				buf += code[pos]
				pos += 1
			if (buf == "println"):
				tokens.append(Token("keyword", buf, -1, []))
			elif (buf == "exit"):
				tokens.append(Token("keyword", buf, 1, []))
			elif (buf == "sum"):
				tokens.append(Token("keyword", buf, -1, []))
			elif (buf == "prod"):
				tokens.append(Token("keyword", buf, -1, []))
			elif (buf == "array"):
				tokens.append(Token("keyword", buf, 1, []))
			else:
				tokens.append(Token("ident", buf, None, None))
			buf = ""
		else:
			while (code[pos] not in (varNames + "0123456789" + " \n\0")):
				buf += code[pos]
				pos += 1
			buf = buf.rstrip()
			if (buf == "["):
				tokens.append(Token("openbr", "", None, None))
			elif (buf == "]"):
				tokens.append(Token("closebr", "", None, None))
			elif (all([i == "]" for i in buf])):
				for i in range(len(buf)):
					tokens.append(Token("closebr", "", None, None))
			buf = ""
		if (code[pos] in " \n\b\t\v"):
			pos += 1

	tokens.append(Token("EOF", "", None, None))
	return tokens

def parse(tokens):
	pos = 0

	astStack = []

	while (tokens[pos].TYPE != "EOF"):
		if (tokens[pos].TYPE == "intlit"):
			assert len(astStack) > 0, f"E001: Trying to write expressions without any container."
			astStack[-1].ARGV.append(tokens[pos].VALUE)
			pos += 1
		elif (tokens[pos].TYPE == "keyword"):
			assert (tokens[pos+1].TYPE == "openbr"), f"E002: Container for expession never opened."
			astStack.append(tokens[pos])
			pos += 2
		elif (tokens[pos].TYPE == "closebr"):
			assert len(astStack) > 0, f"E003: Trying to close the container, but container is never opened."
			event = astStack.pop()
			assert event.TYPE == "keyword", f"PE001: [Parser errors are very rare!]: Trying to evaluate the expression, but found `{event.TYPE}` instead of expression."
			if (event.VALUE == "println"):
				print(*event.ARGV, sep = "")
			elif (event.VALUE == "sum"):
				astStack[-1].ARGV.append(sum(list(map(int, event.ARGV))))
			elif (event.VALUE == "array"):
				astStack[-1].ARGV.append([0] * int(event.ARGV[0]))
			elif (event.VALUE == "prod"):
				astStack[-1].ARGV.append(prod(list(map(int, event.ARGV))))
			pos += 1
		else:
			assert False, f"EGGG: Word `{tokens[pos].VALUE}` is not defined."

cdr = """
	println[sum[val[x] val[y]]]

"""
toks = lex(cdr)
parse(toks)
