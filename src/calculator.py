class CalculatorError(Exception):
    """自定义计算异常，区分业务错误和系统错误"""
    pass

def precedence(op: str) -> int:
    """运算符优先级定义"""
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0

def infix_to_postfix(expression: str) -> list:
    """中缀表达式转后缀表达式（逆波兰式）"""
    expression = expression.replace(" ", "")
    if not expression:
        raise CalculatorError("表达式不能为空")
    
    output = []
    op_stack = []
    i = 0
    n = len(expression)
    
    while i < n:
        char = expression[i]
        
        # 处理数字和小数点
        if char.isdigit() or char == '.':
            num_str = ""
            while i < n and (expression[i].isdigit() or expression[i] == '.'):
                num_str += expression[i]
                i += 1
            if num_str.count('.') > 1:
                raise CalculatorError(f"无效数字格式: {num_str}")
            output.append(float(num_str))
            continue
        
        elif char == '(':
            op_stack.append(char)
        
        elif char == ')':
            while op_stack and op_stack[-1] != '(':
                output.append(op_stack.pop())
            if not op_stack:
                raise CalculatorError("括号不匹配：缺少左括号")
            op_stack.pop()
        
        elif char in ('+', '-', '*', '/'):
            # 处理一元正负号：表达式开头 / 左括号后 / 运算符后
            if (char == '+' or char == '-') and (i == 0 or expression[i-1] in ('(', '+', '-', '*', '/')):
                # 补0转为二元运算，如 -5 -> 0-5，3*-2 -> 3*(0-2)
                output.append(0.0)
                op_stack.append(char)
            else:
                while op_stack and op_stack[-1] != '(' and precedence(op_stack[-1]) >= precedence(char):
                    output.append(op_stack.pop())
                op_stack.append(char)
        
        else:
            raise CalculatorError(f"非法字符: {char}")
        
        i += 1
    
    # 弹出栈中剩余运算符
    while op_stack:
        top = op_stack.pop()
        if top == '(':
            raise CalculatorError("括号不匹配：缺少右括号")
        output.append(top)
    
    return output

def calculate_postfix(postfix: list) -> float:
    """计算后缀表达式"""
    stack = []
    for item in postfix:
        if isinstance(item, float):
            stack.append(item)
        else:
            if len(stack) < 2:
                raise CalculatorError("表达式不完整")
            b = stack.pop()
            a = stack.pop()
            if item == '+':
                stack.append(a + b)
            elif item == '-':
                stack.append(a - b)
            elif item == '*':
                stack.append(a * b)
            elif item == '/':
                if b == 0:
                    raise CalculatorError("除数不能为0")
                stack.append(a / b)
    
    if len(stack) != 1:
        raise CalculatorError("无效表达式")
    
    # 格式化浮点数，如 2.0 显示为 2
    result = stack[0]
    return int(result) if result == int(result) else result

def calculate_expression(expression: str):
    """对外暴露的计算入口"""
    try:
        postfix = infix_to_postfix(expression)
        result = calculate_postfix(postfix)
        return True, result
    except CalculatorError as e:
        return False, str(e)
    except Exception as e:
        return False, f"计算错误: {str(e)}"
