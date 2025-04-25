#This file is used to pre-process input latex expressions
#You only need a "master_convert()"
from latex2sympy2_extended import *
from sympy import simplify



def brackets_balanced(s: str) -> bool:
    """
    Check if the brackets in a latex matches
    Args:
        s(str): the input string
    Return:
        if_balanced(Bool): if matches
    """
    stack = []
    bracket_pairs = {')': '(', ']': '[', '}': '{'}  

    for char in s:
        if char in bracket_pairs.values():  
            stack.append(char)
        elif char in bracket_pairs:         
            if not stack or stack[-1] != bracket_pairs[char]:
                return False  
            stack.pop()        
    return len(stack) == 0  



def remove_non_ascii(text):
    return text.encode("ascii", errors="ignore").decode()

import re
def extract_bracket_content(s:str,bracket_position:int) -> str:
    start_idx=bracket_position

    stack = []
    content = []
    escaped = False
    brace_start=start_idx+1
    brace_depth = 0  
    for i in range(brace_start, len(s)):
        char = s[i]
        if escaped:
            content.append(char)
            escaped = False
            continue
        if char == '\\':
            escaped = True
            content.append(char)
            continue
        if char == '{':
            brace_depth += 1
            content.append(char)
        elif char == '}':
            if brace_depth == 0:
                return ''.join(content),i
            brace_depth -= 1
            content.append(char)
        else:
            content.append(char)

    return None,-1
def find_first_unescaped_brace(s: str) -> int:
    escaped = False
    for i, c in enumerate(s):
        if c == '\\' and not escaped:
            escaped = True
            continue
        if c == '{' and not escaped:
            return i
        escaped = False
    return -1

def extract_command(s: str, brace_pos: int) -> str | None:
    """extract the command name from a bracket"""
    i = brace_pos - 1
    parameter_mode=False
    while i >= 0:
        if not parameter_mode and s[i] in ('^','_'):
            return s[i]
        if not parameter_mode and not s[i] in (' ','\t',']','['):
            break
        if s[i]==']':
            parameter_mode=True
        if s[i]=='[' and parameter_mode:
            parameter_mode=False
        i -= 1
    
    # Start point
    if i < 0 or s[i] == '\\':
        return None
    
    # Extract command name
    command_end = i
    i -= 1
    while i >= 0 and s[i].isalpha():
        i -= 1
    if i<-1 or s[i]!='\\':
        return None
    return s[i+1:command_end+1]


def remove_command(s,command,keep_inside=False):
    pos=s.find(command)
    if pos<0:
        return s
    end_index=pos+len(command)
    level=0
    escaped=False
    #print(end_index,s[end_index])
    if s[end_index]=="{":
        while end_index<len(s):

            if s[end_index]=='{':
                level+=1
            elif s[end_index]=='}':
                level-=1
                if level==0:
                    break
            end_index+=1
    else:
        s1="".join([s[0:pos],s[end_index:]])
    if keep_inside:
        s1="".join([s[0:pos],s[pos+len(command)+1:end_index],s[end_index+1:]])
    else:
        s1="".join([s[0:pos],s[end_index+1:]])
    #print(s1)
    return remove_command(s1,command,keep_inside)
    
import re

def convert_latex_fractions(latex_str):
    """
    Convert non-standard fraction like \frac\alpha2 to its standard-convertable \frac{\alpha}{2}
    We suppoort single letter,number or standard form
    """
    pattern = r'\\frac((?:\\[a-zA-Z]+|\d|[a-zA-Z]|{[^{}]*}))((?:\\[a-zA-Z]+|\d|[a-zA-Z]|{[^{}]*}))'
    
    def replacer(match):
        numerator, denominator = match.group(1), match.group(2)
        wrap_num = f'{{{numerator}}}' if not (numerator.startswith('{') and numerator.endswith('}')) else numerator
        wrap_den = f'{{{denominator}}}' if not (denominator.startswith('{') and denominator.endswith('}')) else denominator
        return fr'\frac{wrap_num}{wrap_den}'
    
    return re.sub(pattern, replacer, latex_str)

    
def get_first_brace_command(s: str) -> str | None:
    """ Find the first brace """
    brace_pos = find_first_unescaped_brace(s)
    if brace_pos == -1:
        return None
    return extract_command(s, brace_pos)
def remove_overall_brace(s:str) -> str:
    """
    Remove the overall {xxx} brace
    """
    pos=find_first_unescaped_brace(s)
    if pos==-1:
        return s,0
    command=get_first_brace_command(s)
    if not command:

        content,final=extract_bracket_content(s,pos)
        #print(s[final])
        if final==len(s) or not '}' in s[final+1:]:
            return content,1
    return s,0


def exp_frac(s):

    def exp_frac_single(s):
        position=s.find("^\\frac")+1
        if position == 0:
            return s
        level=0
        cnt=0
        idx=position
        while idx<len(s):
            if s[idx]=='{':
                cnt+=1
            elif s[idx]=='}':
                cnt-=1
                if cnt==0:
                    level+=1
                    if level==2:
                        break
            idx+=1
        s1="".join([s[0:position],'{',s[position:idx],'}',s[idx:]])
        return s1
    s1=exp_frac_single(s)
    cnt=0
    while s1 != s and cnt<100:
        cnt+=1
        s=s1
        s1=exp_frac_single(s)
    return s



def find_all(s, sub_str, allow_overlap=True):
    indexes = []
    start = 0
    step = 1 if allow_overlap else len(sub_str)
    cnt=0
    while True and cnt<100:
        pos = s.find(sub_str, start)
        if pos == -1:
            break
        indexes.append(pos)
        start = pos + step 
        cnt+=1
    return indexes

def bar_inside_vec(s):
    indices=find_all(s,"\\vec{")
    if not indices:
        return s
    for i in range(len(indices)):
        position=find_all(s,"\\vec{")[i]
        idx=position+4
        #print(s[idx])
        idx2=idx
        level=0
        while idx2<len(s):
            if s[idx2]=='{':
                level+=1
            if s[idx2]=='}':
                level-=1
                if level==0:
                    break
            idx2+=1
    
        s1=s[idx+1:idx2]
        #print(s1)

        s1=remove_command(s1,"\\bar",keep_inside=True)
        s2= "".join([s[0:idx+1],s1,s[idx2:]])
        s=s2
    return s
def vec_lower_idx(input_str):
    """
    in the annoying latex2sympy, error may occur when\ vec{a_{b}},we need\\vec{a_b}
    Args：
        input_str (str): Original string
    
    Return：
        str(str): Converted
    """
    pattern = r'\\vec\{([^{}]+)_{([^{}]+)}\}'
    replacement = r'\\vec{\1}_{\2}'
    return re.sub(pattern, replacement, input_str)
def convert_vec_syntax(text):
    """
    Convert vec to a standard form
    \vec xxx → \vec{xxx}
    \vec α → \vec{α}
    \vec\Gamma → \vec{\Gamma}
    """
    pattern = r'\\vec(\s*)(\\?[a-zA-Zα-ωΑ-Ω]+)'
    replacement = r'\\vec{\2}'
    return re.sub(pattern, replacement, text)

def remove_outer_braces(tex_str):
    """
    convert {base}_{subscript} to base_{subscript}
    Example：
    {a}_{xyz} → a_{xyz}
    {\theta}_{0} → \theta_{0}
    """
    pattern = r'\{(\\(?:[a-zA-Z]+|.)|[^{}])+\}_\{([^}]+)\}'
    return re.sub(pattern, r'\1_{\2}', tex_str)

def extract_last_equal_content(s: str, strip_whitespace: bool = True) -> str:
    """
    Extract content after last equal or sth else.
    
    :param strip_whitespace: （default True）
    """
    final_sign=('=','\\approx','\\ge','\\le','\\geq','\\leq','<','>')

    content=s
    for sign in final_sign:
        if sign in s:
            content=s[s.rfind(sign)+1:]
            break

    return content.strip() if strip_whitespace else content

def first_pre_process(s,extrac_box=True):
    #s=remove_non_ascii(s)
    s=s.replace('\\{','(') 
    s=s.replace('\\}',')')
    if not brackets_balanced(s):
        return s
    if extrac_box:
        boxed_content=remove_command(s,'\\boxed',keep_inside=True)
    else:
        boxed_content=s
    exist_overall_brace=True
    cnt=0
    while exist_overall_brace and cnt<10:
        boxed_content,exist_overall_brace=remove_overall_brace(boxed_content)
        cnt+=1

    if '\\quad' in s:
        s=s.split('\\quad')[0]

    last_equal_content=extract_last_equal_content(boxed_content)

    exist_overall_brace=True
    cnt=0
    while exist_overall_brace and cnt<19:
        last_equal_content,exist_overall_brace=remove_overall_brace(last_equal_content)
        cnt+=1
    return last_equal_content
def second_pre_process(s):
    kill_commands=[
        '\\begin',
        '\\end'
    ]
    remove_commands=[
        '\\text',
        '\\mathbf',
        '\\mathrm',
        '\\pmb',
        '\\hat',
        '\\overline',
        '\\boldsymbol',
    ]


    remove_content=[
        '\\,','$',',','`','latex','\\left','\\right','\\text','\\mathrm','\\Bigr','\\Bigl','\n','\\]','\\[',
        '\\Big','\\bigl','\\bigr','\\biggl','\\biggr','\\displaystyle','\\boldsymbol','\\infty'
    ]
    replace_content=[
        ('\\operatorname{asin}','\\asin'),
        ('\\operatorname{sech}','\\sech'),
        ('\\operatorname{acos}','\\acos'),
        ('\\operatorname{sinh}','\\sinh'),
        ('\\dfrac','\\frac'),
        ('\\tfrac','\\frac'),
        ('\\Exp','\\exp'),
        ('\\times','\\bar{times}'),
        ('\\partial','\\bar{partial}'),
        ('\\perp','\\bar{perp}'),
        ('\\epsilon','\\varepsilon'),
        ('\\varOmega','\\Omega'),
        ('I','\\bar{I}'),
        ('_e','_{e}'),
        ('e_','\\bar{e}_'),
        ('E_','\\bar{E}_'),
        ('\\pm','+'),
        ('\\mp','-'),
        ('{+}','{p}'),
        ("{-}",'{m}'),
        ("_+",'_p'),
        ('_-',"_m")
    ]
    for command in kill_commands:
        s=remove_command(s,command,keep_inside=False)
    for command in remove_commands:
        s=remove_command(s,command,keep_inside=True)
    for content in remove_content:
        s=s.replace(content,'')
    for content in replace_content:
        s=s.replace(content[0],content[1])
    s=convert_latex_fractions(s)
    #print(s)
    s=bar_inside_vec(s)
    s=vec_lower_idx(s)
    s=convert_vec_syntax(s)
    s=exp_frac(s)
    #s=remove_outer_braces(s)
    if s[-1]=='.':
        return s[:-1]
    return s


class MyConfig:
    
    interpret_as_mixed_fractions: bool = False
    interpret_simple_eq_as_assignment: bool = False
    interpret_contains_as_eq: bool = True
    lowercase_symbols: bool = False
    """
    Args:
        interpret_as_mixed_fractions (bool): Whether to interpert 2 \frac{1}{2} as 2/2 or 2 + 1/2
        interpret_simple_eq_as_assignment (bool): Whether to interpret simple equations as assignments k=1 -> 1
        interpret_contains_as_eq (bool): Whether to interpret contains as equality x \\in {1,2,3} -> x = {1,2,3}
        lowercase_symbols (bool): Whether to lowercase all symbols
    """
class MyNormalization:
    """Configuration for latex normalization.
    
    Each field controls a group of related normalizations:
    - basic_latex: Basic latex command replacements (mathrm, displaystyle, etc.)
    - units: Remove units and their variations
    - malformed_operators: Fix malformed operators (sqrt, frac, etc.)
    - nits: Small formatting fixes (spaces, dots, etc.)
    - boxed: Extract content from boxed environments
    - equations: Handle equation splitting and approximations (deprecated)
    """
    basic_latex: bool = True
    units: bool = False
    malformed_operators: bool = True
    nits: bool = True
    boxed = "all"
    equations: bool = False

def master_convert(s):
    """
    The only function needed
    Args:
        s(str): the input string
    Return:
        Sym(Sympy Expression): the output sympy string
    """
    s1=first_pre_process(s)

    s2=second_pre_process(s1)

    Sym=latex2sympy(s2,normalization_config=MyNormalization(),conversion_config=MyConfig)
    return Sym
