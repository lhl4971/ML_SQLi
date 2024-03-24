import re
import pandas as pd
from binary_sub import binary_sub

class Tokenizer:
    def __init__(self):
        self.keywords = []
        self.functions = []
        self.keywords_path = "./resource/keywords.csv"
        self.functions_path = "./resource/functions.csv"
        self.spec_char = ["NEQ", "AND", "OR", "CMTST", "CMTEND", "TLDE", "EXCLM", "ATR", "HASH", "DLLR", "PRCNT", "XOR", "BITAND", "BITOR", "STAR", "MINUS", "PLUS", "EQ", "LPRN", "RPRN", "LCBR", "RCBR", "LSQBR", "RSQBR", "BSLSH", "CLN", "SMCLN", "DQUT", "SQUT", "LT", "GT", "CMMA", "DOT", "QSTN", "SLSH"]
        self.reserved_tokens = ["CHR", "STR", "HEX", "DEC", "INT", "IPADDR"]
        self._read_keywords()
        self._read_functions()

    def import_query(self, str=""):
        self.str = ' ' + str + ' '

    def get_str(self):
        return self.str

    def _read_keywords(self):
        kw = pd.read_csv(self.keywords_path)
        self.keywords = kw['Name']
        self.keywords[412] = "NULL"
        self.keywords = self.keywords.sort_index().to_list()
    
    def get_keywords(self):
        return self.keywords

    def _read_functions(self):
        fc = pd.read_csv(self.functions_path)
        self.functions = fc['Name']
        for i in range(0,len(self.functions)):
            self.functions[i] = self.functions[i][:-2].upper()
        self.functions = self.functions.sort_index().to_list()
    
    def get_functions(self):
        return self.functions
    
    def _remove_parentheses(self):
        stack = []
        for i, c in enumerate(self.str):
            if c != ')':
                stack.append(i)
            else:
                j=-1
                if stack:
                    while(self.str[stack[j]] != '(' and j>-len(stack)):
                        j-=1
                    if(self.str[stack[j]] == '('):
                        del stack[j]
                    else:
                        stack.append(i)
                else:
                    stack.append(i)
        result = ''
        for i, c in enumerate(self.str):
            if i in stack:
                result += c
        self.str = result

    def _sub_char(self):
        str = self.str
        str = str.replace("`", " ")
        str = str.replace("!=", " NEQ ")
        str = str.replace("<>", " NEQ ")
        str = str.replace("&&", " AND ")
        str = str.replace("||", " OR ")
        str = str.replace("/*", " CMTST ")
        str = str.replace("*/", " CMTEND ")
        str = str.replace("~", " TLDE ")
        str = str.replace("!", " EXCLM ")
        str = str.replace("@", " ATR ")
        str = str.replace("#", " HASH ")
        str = str.replace("$", " DLLR ")
        str = str.replace("%", " PRCNT ")
        str = str.replace("^", " XOR ")
        str = str.replace("&", " BITAND ")
        str = str.replace("|", " BITOR ")
        str = str.replace("*", " STAR ")
        str = str.replace("-", " MINUS ")
        str = str.replace("+", " PLUS ")
        str = str.replace("=", " EQ ")
        str = str.replace("(", " LPRN ")
        str = str.replace(")", " RPRN ")
        str = str.replace("{", " LCBR ")
        str = str.replace("}", " RCBR ")
        str = str.replace("[", " LSQBR ")
        str = str.replace("]", " RSQBR ")
        str = str.replace("\\", " BSLSH ")
        str = str.replace(":", " CLN ")
        str = str.replace(";", " SMCLN ")
        str = str.replace("\"", " DQUT ")
        str = str.replace("'", " SQUT ")
        str = str.replace("<", " LT ")
        str = str.replace(">", " GT ")
        str = str.replace(",", " CMMA ")
        str = str.replace(".", " DOT ")
        str = str.replace("?", " QSTN ")
        str = str.replace("/", " SLSH ")
        self.str = str

    #delete White-space characters
    def _del_white_space_char(self):
        self.str = self.str.replace("\t", " ").replace("\n", " ").replace("\r", " ")

    #delete Empty comments
    def _del_empty_comments(self):
        str = self.str
        while(True):
            new_str = re.sub(r'\/\*(\s*)\*\/',' ',str)
            if(new_str == str):
                break
            str = new_str
        self.str = str

    #Substitute Decimal value (Float number and Scientific Notation)
    def _sub_dec(self):
        self.str = re.sub(r'[+-]?[1-9]\.[0-9]+E[+-]?[0-9]+',' DEC ', self.str)
        self.str = re.sub(r'[+-]?[0-9]+\.[0-9]+',' DEC ', self.str)

    #Substitute SQL keywords, and reserved words
    def _sub_keywords(self):
        self.str = binary_sub(self.str, self.keywords, "keywords")

    #Substitute SQL keywords, and reserved words
    def _sub_functions(self):
        self.str = binary_sub(self.str, self.functions, "functions")

    #Substitute IPv4 and IPv6 addresses
    def _sub_ip(self):
        self.str = re.sub(r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}',' IPADDR ', self.str)
        self.str = re.sub(r'\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*',' IPADDR ', self.str)

    #Substitute Hexadecimal value
    def _sub_hex(self):
        self.str = re.sub(r'\s+0x[0-9a-fA-F]+',' HEX ', self.str)

    #Substitute Integer value
    def _sub_int(self):
        self.str = re.sub(r'\s+[0-9]+',' INT ', self.str)

    #Substitute Multiple spaces
    def _sub_multi_spaces(self):
        self.str = re.sub(r'\s+',' ',self.str)
        self.str = self.str.strip()

    #Substitute all others by CHR and STR
    def _sub_others(self):
        str = self.str
        str = str.split()
        for i in range(0, len(str)):
            if(not ((str[i] in self.reserved_tokens) or (str[i] in self.spec_char) or (str[i] in self.keywords) or (str[i][2:] in self.functions) and (str[i][:2] == 'F_'))):
                if(len(str[i]) == 1):
                    str[i] = "CHR"
                else:
                    str[i] = "STR"
        self.str = str

    #Substitute 'CHR DOT STR' and 'STR DOT STR' by 'STR'
    def _sub_sds(self):
        str = self.str
        str = ' '.join(str)
        while(True):
            new_str = re.sub(r'CHR DOT STR','STR',str)
            new_str = re.sub(r'STR DOT STR','STR',new_str)
            if(new_str == str):
                break
            str = new_str
        self.str = str

    #Exercise all substitution in order
    def tokenization(self):
        self._del_white_space_char()
        self._del_empty_comments()
        self._remove_parentheses()
        self._sub_dec()
        self._sub_char()
        self._sub_keywords()
        self._sub_functions()
        self._sub_ip()
        self._sub_hex()
        self._sub_int()
        self._sub_multi_spaces()
        self._sub_others()
        self._sub_sds()

    #Return a list of all tokens
    def get_token_list(self):
        tmp_func = self.get_functions().copy()
        for i in range(len(tmp_func)):
            tmp_func[i] = ("F_" + tmp_func[i]).upper()
        token_list = self.reserved_tokens + self.spec_char + self.keywords + tmp_func
        token_list.sort()
        return token_list
