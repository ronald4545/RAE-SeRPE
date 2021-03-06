"""
Date: Thu, 9 Feb, 2017
Last updated: Sat, 6 Mar, 2017
Author: Samuel Barham
Organization: University of Maryland, College Park (PhD student)

Project: RAE/SeRPE implementation
Component: Planning-DSL Interpreter

Description:
The interpreter exists to read in, parse, store, method files (whose content is
written in a simple domain-specific language) and to aid in executing the
tasks and methods they define. The first three functions mentioned (reading in,
parsing, and storing) are handled by the lexer/parser pair, which are built atop
the popular PLY (Pytnon Lex-Yacc). Their rules are defined in the files
lexer.py and parser.py, respectively. Whereas a lexer is built to
understand the lexical structure of a language, and a parser is built to under-
stand its grammatical structure (a higher level of organization), the
interpreter exists to attach a semantics to the grammatical structure captured
by the parser. The interpreter is written by hand, from scratch, unlike the
lexer and parser, because it is simple and the resulting code is transparent
enough -- and this gives us a greater degree of control over the interpreter's
semantics and operation.

More information on the PLY module used to build the the lexer and the parser
can be found at the following URL:
http://www.dabeaz.com/ply/ply.html#ply_nn1

_________________

Finally, some ideas that we might consider future TODO's:
1) finish implementing local variable read/write for method bodies
2) write a lexer for domain description files, and design the lexer to
    construct a symbol table that it then passes to the method-file parser,
    so that we can check at compile-time that state variables are accessed
    with the proper number of arguments
3) enhance the domain description files and the dom-parser to construct a typed
    symbol table that is then supplied to the method-file parser, so that we can
    check at compile-time for type-consistency in the use of state variables
    (e.g., predicates appear only in boolean expressions, int/float-state vars
    only appear in numerical operations, etc.)

__________________
TODO:
1) write the dom-lexer and dom-parser that generate the state-variable tables
    and domain descriptions used by the interpreter and other planning components.
2) do num 3 above
4) have interpreter disambiguate between state-vars and tasks using the task
    table
6) make environment/state variables a global object, so that planning domain
    state is preserved after recursive method calls
"""

# import statements here
from __future__ import print_function   # this is so that print() will be a
                                        # a function, rather than a statement --
                                        # in Pytnon 2.x, print() is merely a
                                        # statement; in Pytnon 3.x, it is an
                                        # actual function -- which allows us
                                        # to use it in lambdas, which expect
                                        # expressions, not statements
import ply.lex as lex
import ply.yacc as yacc
from pydoc import pager     # we'll be using this to produce less-like,
                            # paged output -- primarily for debugging purposes
# import dom_lexer            # this is the module where we've specified the dom-file lexer rules
# import dom_parser           # this is the module where we've specified the dom-file parser rules
import parsing.meth_lexer           # this is the module where we've specified the method-file lexer rules
import parsing.meth_parser as meth_parser         # this is the module where we've specified the method-file parser rules
# import pprint             # python's pretty-printer for arbitrary data
import json                 # a better way of getting a pretty print of a dict
import cPickle as pickle    # for serializing objects to file -- in our case,
                            # we'll want to be persisting our method tables
from collections import deque


"""
EXPRESSION TYPES

The following hash defines the types of expressions in the byte-code used
by the intrepeter. The comments after each expression type lists their
arguments, and the types of those arguments, for the developer's convenience.
For now, we only list the types that have been actually implemented in the
parser, so as not to confuse:
"""

e_types = dict(
    # misc
    e_noop =    'NOOP',     # [no arguments]
    # statements
    e_seq =     'SEQ',      # local_variables (list), exprs (list)
    e_while =   'WHILE',    # cond (expr), exprs (list)
    e_if =      'IF',       # conds (expr list), blocks (list of lists of exprs)
    # binary operators
    e_and =     'AND',      # arg1 (expr), arg2 (expr)
    e_or =      'OR',       # "    "       "    "
    e_equals =  'EQUALS',   # "    "       "    "
    e_lt =      'LT',       # "    "       "    "
    e_gt =      'GT',       # "    "       "    "
    e_lte =     'LTE',      # "    "       "    "
    e_gte =     'GTE',      # "    "       "    "
    # unary operators
    e_not =     'NOT',      # arg1 (expr)
    # primitive values
    e_true =    'TRUE',     # arg1 (True)
    e_false =   'FALSE',    # arg1 (False)
    # variable expressions
    e_state_var_rd =    'STATE_VAR_RD',     # arg1 (id string),
                                            # arg2 (list of parameter ids)
    e_state_var_wr =    'STATE_VAR_WR',     # arg1 (id string),
                                            # arg2 (list of parameter ids)
                                            # arg3 (expr)
    e_loc_var_rd =      'LOC_VAR_RD',       # arg1 (id string)
    e_loc_var_wr =      'LOC_VAR_WR'        # arg1 (id string), arg2 (expr)
)

"""
SINGLETON VALUES
"""

val_none = dict(
    v_type = 'val_none',
    val = None
)

"""
AUXILIARY CLASSES

For now, we'll just put here any errors that the interpreter may need to raise.
Perhaps, at a later date, we may wish to factor these out into a separate
file.
"""

class NoMethodTable(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MethodNotFound(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NoMethodSupplied(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class SemanticError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NoSuchInstruction(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

"""
INTERPRETER CLASS

This class encapsulates a pair (I, M), where I is an interpreter and M is a
method. The reason for writing the class in this way -- that is, for requiring
an interpreter instance always to be paired with a method instance is that by
this device, we gain the ability to iterate over an interpreter instance,
treating it as if it were a list of decision-tree nodes.
"""

class Interpreter:
    def __init__(self, method = {}, environment = {},
                 state_vars = {}, task_table = {}, action_table = {},
                 mode = 'SeRPE'):
        self.method = method
        self.environment = environment
        self.state_vars = state_vars
        self.task_table = task_table
        self.action_table = action_table
        self.mode = mode # can be SeRPE or RAE
        self.new_decision_node = False
        self.decision_node = None
        self.action_result = None
        self.ret = (val_none, environment, state_vars)
        self.state = 'READY' # can be READY, ACTING, FINISHED, or ERROR
        self.stack = deque([])

        # print("\n\nenvironment = " + environment.__repr__() + "\n\n")

    def __iter__(self):
        return self

    def next(self):
        # print("\n\nin next again!\n\n")
        # if we just finished performing an action,
        # catch the result
        if self.mode == 'ACTING':
            # print("\n\nHERE!!!\n\n")
            self.mode = 'EXECUTING'

            # interpret the result
            v_type = 'val_none'
            if isinstance(self.action_result, str):
                v_type = 'val_str'
            elif isinstance(self.action_result, (int, float, long)):
                v_type = 'val_num'
            elif isinstance(self.action_result, bool):
                v_type = 'val_bool'

            action_result = dict(
                v_type = v_type,
                val = self.action_result
            )
            self.ret = (action_result, self.environment, self.state_vars)

        # continue executing the method
        if self.new_decision_node:
            # print("\n\nreturning decision node!\n\n")
            self.new_decision_node = False
            return self.decision_node
        elif self.stack: # pick up where we left off
            next_instr, environment = self.stack.popleft()
            self.eval(next_instr, environment, self.state_vars)
            # print("\n\nherein 'elif self.stack'!\n\n")
            return self.next()
        elif self.state == 'READY' or self.state == 'EXECUTING':
            self.execute_method(self.method, self.environment, self.state_vars)
            # print("\n\nherein 'elif self.state'!\n\n")
            return self.next()
        else:
            self.state = 'FINISHED'
            raise StopIteration

    # def __str__(self):
    #     return json.dumps(self.decision_nodes, sort_keys=False, indent=3)


    #NOTE: THIS DOCUMENTATION NEEDS TO BE REWRITTEN IN LIGHT OF RECENT CHANGES
    """
    INTERPRETER API

    The following functions provide an API for the interpreter module. In general,
    to invoke the interpreter, one must either first ensure that a method file has
    been loaded into memory (the load_methods(<filename>) function handles this),
    which generates a method-table; or one must already
    """

    def execute_method(self, method, environment, state_vars):
        print("\n\nHERE!\n\n")
        self.state = 'EXECUTING'
        if method:
            first_instr = method['exprs']
            return self.eval(first_instr, environment=environment,
                             state_vars=state_vars)
        else:
            raise NoMethodSupplied("No valid method specified for execution")

    def execute_method_name(self, method_name, environment,
                       method_table = meth_parser.get_method_table()):
        """
        Looks up the supplied method name in the method table and attempts to
        execute the corresponding byte-code sequence. If the method is not found,
        execute_method() raises a MethodNotFound error. If the method table is not
        supplied, execute_method() attempts to get the most recently compiled
        method table from the parser module. If this fails, the method raises
        a NoMethodTable error.

        By default, execution begins at the first instruction in the body of
        the method.

        (* Note -- the following is currently not supported: If necessary, the
        invoking function can pass in an instruction index to begin execution at any
        arbitrary point in the method body -- as, for instance, when resuming
        execution after backtracking. *)

        When execution reaches the end of the method, a tuple is returned
        containing, as the first component, the environment at the end of
        method execution, and, as the second component, the return value of the
        method -- which, for void methods, is None.

        During execution of the method, the interpreter executes the byte-code
        instructions found in the method table one by one, in sequence, until
        it encounters a decision point, which we define for now as a task-
        invocation. At that point, the interpreter should yield to the invoking
        function a tuple containing the current task-node, the current domain
        state (i.e., the set of all state variable assignments), and the current
        environment state (i.e., the set of all local variable assignments).

        In the future, we may wish to support planning over non-deterministic
        action outcomes, in which case we will also wish to yield action-nodes
        as decision points in the planning tree.
        """
        # no method table yet
        if not method_table:
            raise NoMethodTable("Either the method table you supplied is empty, " \
                                 "or it is nil, or no .meth file has been parsed yet")

        # no such method
        method = method_table.get(method_name)
        if not method:
            raise MethodNotFound("No such method exists: '{0}'".format(method_name))

        # method table and method exist -- execute method
        return execute_method(method, environment, state_vars)

    def _raise_no_such_instruction(self, curr_instr, environment, state_vars):
        raise NoSuchInstruction("instruction '{0}' does not exist". \
                                 format(curr_instr['e_type']))

    def eval(self, curr_instr, environment, state_vars):
        print("In eval with curr_instr = " + repr(curr_instr))
        op_sem = {
            'E_NOOP':         self.e_noop,
            'E_FAIL':         self.e_fail,
            'E_SEQ':          self.e_seq,
            'E_WHILE':        self.e_while,
            'E_IF':           self.e_if,
            'E_AND':          self.e_and,
            'E_OR':           self.e_or,
            'E_EQUALS':       self.e_equals,
            'E_LT':           self.e_lt,
            'E_GT':           self.e_gt,
            'E_LTE':          self.e_lte,
            'E_GTE':          self.e_gte,
            'E_NOT':          self.e_not,
            'E_TRUE':         self.e_true,
            'E_FALSE':        self.e_false,
            'E_INT':          self.e_int,
            'E_FLOAT':        self.e_float,
            'E_ADD':          self.e_add,
            'E_SUB':          self.e_sub,
            'E_MUL':          self.e_mul,
            'E_DIV':          self.e_div,
            'E_STRING':       self.e_string,
            'E_STATE_VAR_RD': self.e_state_var_rd,
            'E_STATE_VAR_WR': self.e_state_var_wr,
            'E_LOC_VAR_RD':   self.e_loc_var_rd,
            'E_LOC_VAR_WR':   self.e_loc_var_wr,
            'E_TASK_INVOCATION':  self.e_task_invocation
        }.get(curr_instr['e_type'], self._raise_no_such_instruction)

        # before proceeding with execusion, check if there are any new
        # decision nodes to yield
        # if self.new_decision_node:
        #     print("caught decision node = " + self.decision_node.__repr__() + "\n")
        #     self.stack.append((curr_instr, environment))
        #     pass

        # print("recursing on ast")
        # continue recursing on the AST
        op_sem(curr_instr, environment=environment, state_vars=state_vars)
        # print("done recursing on ast")


    """
    PRIVATE METHODS
    """

    """
    OPERATIONAL SEMANTICS

    The following functions define the semantics of the interpreter's instruction
    set. Generally, the semantics reduces expressions in the method-file language's
    expression grammar to values (represented as native Python values).
    """

        # noop
    def e_noop(self, instr, environment, state_vars):      # [no arguments]
        # self.state = 'FINISHED'
        # if self.ret:
        #     pass
        # else:
        #     self.ret = (None, environment, state_vars)
        pass

    def e_fail(self, instr, environment, state_vars):
        self.new_decision_node = True
        self.decision_node = ('FAIL', 'FAIL', 'FAIL')


    """
    IMPORTANT NOTE
    """
        # sequence and control statement instructions
    def e_seq(self, instr, environment, state_vars):
        this_instr = instr['arg1']
        next_instr = instr['arg2']
        self.eval(this_instr, environment=environment,
                              state_vars=state_vars)
        (res, environment, state_vars) = self.ret

        # we might have generated a decision node in executing that instr;
        # if so, save the execution state and pass so that the original invok
        # ing method (__next__) can yield the decision node
        if self.new_decision_node:
            # print("\ncaught decision node in seq!\n\n")
            # print("self.mode = " + self.mode)
            self.stack.append((next_instr, environment))
            return
        # elif self.mode == 'RAE' and not self.new_decision_node:
        #     self.new_decision_node = True
        #     self.decision_node = dict(
        #                             node_type =   'progress_node',
        #                             environment = environment,
        #                             state_vars = state_vars
        #                          )

        self.eval(next_instr, environment=environment,
                              state_vars=state_vars)

    def e_while(self, instr, environment, state_vars):
        cond = instr['cond']
        block = instr['block']
        self.eval(cond, environment=environment, state_vars=state_vars)
        (cond_res, _, _) =  self.ret
        ret = val_none
        while cond_res['val']:
            # evaluate the code block once
            self.eval(block, environment=environment,
                             state_vars=state_vars)
            (ret, environment, state_vars) = self.ret

            # there could be a new decision node after evaluating the block
            if self.new_decision_node:
                self.stack.append((instr, environment)) # save the state
                return # return so that __next__ (the original invoking method)
                     # can yield the generated decision node

            # now evaluate the guard and continue iterating as appropriate
            self.eval(cond, environment=environment,
                            state_vars=state_vars)
            (cond_res, _, _) = self.ret

        self.ret = (ret, environment, state_vars)

    def e_if(self, instr, environment, state_vars):
        cond_list = instr['conds']
        block_list = instr['blocks']

        # print("got cond list: \n")
        # print(dump(cond_list) + "\n")
        #
        # print("got block list: \n")
        # print(dump(block_list) + "\n")

        i = 0;
        while i < len(cond_list):
            cond = cond_list[i]
            block = block_list[i]
            # print("in if with cond = " + cond.__repr__())

            self.eval(cond, environment=environment,
                            state_vars=state_vars)
            (res, _, _) = self.ret

            if res['val']:
                # print("cond succeeded; in block = " + block.__repr__())
                self.eval(block, environment=environment,
                                 state_vars=state_vars)
                return

            i = i + 1;

        self.ret = (val_none, environment, state_vars)

        # binary (here only boolean) operators
    def e_and(self, instr, environment, state_vars):
        l_expr = instr['arg1']
        r_expr = instr['arg2']

        self.eval(l_expr, environment=environment,
                          state_vars=state_vars)
        (l_res, _, _) = self.ret
        self.eval(r_expr, environment=environment,
                          state_vars=state_vars)
        (r_res, _, _) = self.ret

        if l_res['v_type'] == 'val_bool' and r_res['v_type'] == 'val_bool':
            l_operand, r_operand = l_res['val'], r_res['val']
            self.ret = (dict(
                            v_type = 'val_bool',
                            val = l_operand and r_operand
                        ), environment, state_vars)
        else:
            raise TypeError("Error near logical 'and' ('&&'): both operand expressions \
                             must be of type boolean")

    def e_or(self, instr, environment, state_vars):
        l_expr = instr['arg1']
        r_expr = instr['arg2']

        self.eval(l_expr, environment=environment,
                          state_vars=state_vars)
        (l_res, _, _) = self.ret
        self.eval(r_expr, environment=environment,
                          state_vars=state_vars)
        (r_res, _, _) = self.ret

        if l_res['v_type'] == 'val_bool' and r_res['v_type'] == 'val_bool':
            l_operand, r_operand = l_res['val'], r_res['val']
            self.ret = (dict(
                            v_type = 'val_bool',
                            val = l_operand or r_operand
                        ), environment, state_vars)
        else:
            raise TypeError("Error near logical 'or' ('||'): both operand expressions \
                             must be of type boolean")

    def e_equals(self, instr, environment, state_vars):
        l_expr = instr['arg1']
        r_expr = instr['arg2']

        self.eval(l_expr, environment=environment,
                          state_vars=state_vars)
        (l_res, _, _) = self.ret
        self.eval(r_expr, environment=environment,
                          state_vars=state_vars)
        (r_res, _, _) = self.ret

        # print("l_expr = " + l_expr.__repr__() + "\n")
        # print("r_expr = " + r_expr.__repr__() + "\n\n")
        # print("l_res = " + l_res.__repr__() + "\n")
        # print("r_res = " + r_res.__repr__() + "\n\n")

        if l_res['v_type'] == r_res['v_type']:
            l_operand, r_operand = l_res['val'], r_res['val']
            self.ret = (dict(
                            v_type = 'val_bool',
                            val = l_operand == r_operand
                        ), environment, state_vars)
        else:
            raise TypeError("Error near '==': both operand expressions \
                             must be of the same type")

    def e_lt(self, instr, environment, state_vars):
        l_expr = instr['arg1']
        r_expr = instr['arg2']

        self.eval(l_expr, environment=environment,
                          state_vars=state_vars)
        (l_res, _, _) = self.ret
        self.eval(r_expr, environment=environment,
                          state_vars=state_vars)
        (r_res, _, _) = self.ret

        if l_res['v_type'] == 'val_num' and r_res['v_type'] == 'val_num':
            l_operand, r_operand = l_res['val'], r_res['val']
            self.ret = (dict(
                            v_type = 'val_bool',
                            val = l_operand < r_operand
                        ), environment, state_vars)
        else:
            raise TypeError("Error near '<': both operand expressions \
                             must be of type numeric")

    def e_gt(self, instr, environment, state_vars):
        l_expr = instr['arg1']
        r_expr = instr['arg2']

        self.eval(l_expr, environment=environment,
                          state_vars=state_vars)
        (l_res, _, _) = self.ret
        self.eval(r_expr, environment=environment,
                          state_vars=state_vars)
        (r_res, _, _) = self.ret

        if l_res['v_type'] == 'val_num' and r_res['v_type'] == 'val_num':
            l_operand, r_operand = l_res['val'], r_res['val']
            self.ret = (dict(
                            v_type = 'val_bool',
                            val = l_operand > r_operand
                        ), environment, state_vars)
        else:
            raise TypeError("Error near '>': both operand expressions \
                             must be of type numeric")

    def e_lte(self, instr, environment, state_vars):
        l_expr = instr['arg1']
        r_expr = instr['arg2']

        self.eval(l_expr, environment=environment,
                          state_vars=state_vars)
        (l_res, _, _) = self.ret
        self.eval(r_expr, environment=environment,
                          state_vars=state_vars)
        (r_res, _, _) = self.ret

        if l_res['v_type'] == 'val_num' and r_res['v_type'] == 'val_num':
            l_operand, r_operand = l_res['val'], r_res['val']
            self.ret = (dict(
                            v_type = 'val_bool',
                            val = l_operand <= r_operand
                        ), environment, state_vars)
        else:
            raise TypeError("Error near '<=': both operand expressions \
                             must be of type numeric")

    def e_gte(self, instr, environment, state_vars):
        l_expr = instr['arg1']
        r_expr = instr['arg2']

        self.eval(l_expr, environment=environment,
                          state_vars=state_vars)
        (l_res, _, _) = self.ret
        self.eval(r_expr, environment=environment,
                          state_vars=state_vars)
        (r_res, _, _) = self.ret

        if l_res['v_type'] == 'val_num' and r_res['v_type'] == 'val_num':
            l_operand, r_operand = l_res['val'], r_res['val']
            self.ret = (dict(
                            v_type = 'val_bool',
                            val = l_operand >= r_operand
                        ), environment, state_vars)
        else:
            raise TypeError("Error near '>=': both operand expressions \
                             must be of type numeric")

        # unary operators
    def e_not(self, instr, environment, state_vars):
        expr = instr['arg1']

        self.eval(expr, environment=environment,
                        state_vars=state_vars)
        (res, _, _) = self.ret

        if res['v_type'] == 'val_bool':
            self.ret = (dict(
                            v_type = 'val_bool',
                            val = not res['val']
                        ), environment, state_vars)
        else:
            raise TypeError("Error near unary not: negated operand expression \
                             must be of type boolean")

        # primitive values
    def e_true(self, instr, environment, state_vars):
        self.ret = (dict(
                        v_type = 'val_bool',
                        val = True
                    ), environment, state_vars)

    def e_false(self, instr, environment, state_vars):
        self.ret = (dict(
                        v_type = 'val_bool',
                        val = False
                    ), environment, state_vars)

    def e_int(self, instr, environment, state_vars):
        # print("IN e_int!")
        self.ret = (dict(
                        v_type = 'val_num',
                        val = instr['val']
                    ), environment, state_vars)
        # print("SET self.ret = " + repr(self.ret))

    def e_float(self, instr, environment, state_vars):
        self.ret = (dict(
                        v_type = 'val_num',
                        val = instr['val']
                    ), environment, state_vars)

    def e_add(self, instr, environment, state_vars):
        l_expr = instr['arg1']
        r_expr = instr['arg2']

        self.eval(l_expr, environment=environment, state_vars=state_vars)
        (l_res, _, _) = self.ret
        self.eval(r_expr, environment=environment, state_vars=state_vars)
        (r_res, _, _) = self.ret

        if l_res['v_type'] == 'val_num' and r_res['v_type'] == 'val_num':
            l_operand, r_operand = l_res['val'], r_res['val']
            self.ret = (dict(
                            v_type = 'val_num',
                            val = l_operand + r_operand
                        ), environment, state_vars)
        else:
            raise TypeError("Error near '+': both operand expressions \
                             must be of type numerical")

    def e_sub(self, instr, environment, state_vars):
        l_expr = instr['arg1']
        r_expr = instr['arg2']

        self.eval(l_expr, environment=environment,
                          state_vars=state_vars)
        (l_res, _, _) = self.ret
        self.eval(r_expr, environment=environment,
                          state_vars=state_vars)
        (r_res, _, _) = self.ret

        if l_res['v_type'] == 'val_num' and r_res['v_type'] == 'val_num':
            l_operand, r_operand = l_res['val'], r_res['val']
            self.ret = (dict(
                            v_type = 'val_num',
                            val = l_operand - r_operand
                        ), environment, state_vars)
        else:
            raise TypeError("Error near '-': both operand expressions \
                             must be of type numerical")

    def e_mul(self, instr, environment, state_vars):
        l_expr = instr['arg1']
        r_expr = instr['arg2']

        self.eval(l_expr, environment=environment,
                          state_vars=state_vars)
        (l_res, _, _) = self.ret
        self.eval(r_expr, environment=environment,
                          state_vars=state_vars)
        (r_res, _, _) = self.ret

        if l_res['v_type'] == 'val_num' and r_res['v_type'] == 'val_num':
            l_operand, r_operand = l_res['val'], r_res['val']
            self.ret = (dict(
                            v_type = 'val_num',
                            val = l_operand * r_operand
                        ), environment, state_vars)
        else:
            raise TypeError("Error near '*': both operand expressions \
                             must be of type numerical")

    def e_div(self, instr, environment, state_vars):
        l_expr = instr['arg1']
        r_expr = instr['arg2']

        self.eval(l_expr, environment=environment,
                          state_vars=state_vars)
        (l_res, _, _) = self.ret
        self.eval(r_expr, environment=environment,
                          state_vars=state_vars)
        (r_res, _, _) = self.ret

        if l_res['v_type'] == 'val_num' and r_res['v_type'] == 'val_num':
            l_operand, r_operand = l_res['val'], r_res['val']
            self.ret = (dict(
                            v_type = 'val_num',
                            val = l_operand / r_operand
                        ), environment, state_vars)
        else:
            raise TypeError("Error near '/': both operand expressions \
                             must be of type numerical")

    def e_string(self, instr, environment, state_vars):
        self.ret = (dict(
                        v_type = 'val_str',
                        val = instr['val']
                    ), environment, state_vars)

        # variable expressions

    """
    THE FOLLOWING COMMENT IS IMPORTANT AND CONTAINS AN IMPLICIT TODO
    """
    # NOTE: we disambiguate between a state-variable read, a task invocation,
    # and an action invocation within the body of this method -- this is a bit
    # kludgie, and we may wish to later rely on a symbol-table constructed by
    # the dom-lexer (which doesn't yet exist) to disambiguate this within the
    # parser and issue separate byte-code instructions; but for now, this will
    # at least work.
    def _eval_helper(self, arg, environment, state_vars):
        # print("in eval_helper evaluating arg = " + arg.__repr__())
        self.eval(arg, environment, state_vars)
        (res, _, _) = self.ret
        return res

    def e_state_var_rd(self, instr, environment, state_vars):  # arg1 (id string), arg2 (list of parameter ids)
        # print("in state_var_rd with instr = " + instr.__repr__())
        id = instr['arg1']
        arguments = instr['arg2']
        evaluated_arguments = tuple([self._eval_helper(arg, environment, state_vars)['val'] \
                                     for arg in arguments])

        # print("\n\ntask_table = " + self.task_table.__repr__() + "\n\n")

        if id in self.task_table:
            task = self.task_table[id]
            # print("hit task " + id + " = " + task.__repr__() + "\n")
            if not len(arguments) == len(task['parameters']):
                raise SemanticError("Task {0} invoked with improper number of \
                                     arguments ({1} rather than {2})".format(id,
                                        arguments.size, task['parameters'].size))

            task_node = ('TASK', id, evaluated_arguments)

            self.decision_node = task_node
            self.new_decision_node = True
            self.ret = (val_none, environment, state_vars)
        elif id in self.action_table:
            action_node = ('ACTION', id, evaluated_arguments)
            # print("\nissuing an action node = " + action_node.__repr__() + "\n")

            self.decision_node = action_node
            self.new_decision_node = True
            self.mode = 'ACTING'
            self.ret = (val_none, environment, state_vars)
        else: # it's a state variable (we hope)
            # print("\n\n\twe were passed state_vars = \n" + state_vars.__repr__() + "\n\n")
            # print("id = " + id + "\n\n")
            # print("evaluated_arguments = " + evaluated_arguments.__repr__() + "\n\n")
            val = state_vars[id][evaluated_arguments]

            v_type = 'val_none'
            if isinstance(val, str):
                v_type = 'val_str'
            elif isinstance(val, (int, float, long)):
                v_type = 'val_num'
            elif isinstance(val, bool):
                v_type = 'val_bool'

            self.ret = (dict(
                            v_type = v_type,
                            val = val
                        ), environment, state_vars)

    def e_state_var_wr(self, instr, environment, state_vars):  # arg1 (id string), arg2 (list of parameter ids), arg3 (expr)
        id = instr['arg1']
        arguments = instr['arg2']

        self.eval(instr['arg3'], environment=environment,
                                 state_vars=state_vars)
        (res, _, state_vars) = self.ret

        state_vars[id][arguments] = res['val']
        self.ret = (res, environment, state_vars)

    def e_loc_var_rd(self, instr, environment, state_vars):    # arg1 (id string)
        # print ("in loc_var_rd with instr = " + instr.__repr__())
        id = instr['arg1']
        val = environment[id]

        v_type = 'val_none'
        if isinstance(val, str):
            v_type = 'val_str'
        elif isinstance(val, (int, float, long)):
            v_type = 'val_num'
        elif isinstance(val, bool):
            v_type = 'val_bool'

        self.ret = (dict(
                        v_type = v_type,
                        val = val
                    ), environment, state_vars)

    def e_loc_var_wr(self, instr, environment, state_vars):    # arg1 (id string), arg2 (expr)
        id = instr['arg1']

        if not self.mode == 'ACTED':
            # print("\n\nabout to evaluate rhs of assignment\n")
            self.eval(instr['arg2'], environment=environment, state_vars=state_vars)
            # print("just evaluated rhs of assignment\n")
            if self.new_decision_node:
                # print("caught new decision node = " + self.decision_node.__repr__())
                # print("self.mode = " + self.mode)
                self.stack.append((instr, environment))
                # print("\n\nstack now looks like: = " + dump(self.stack) + "\n\n")
                #pass
                #print("\n\nwent past pass??\n\n")
                return
            # else:
                # print("failed to generate decision node")
        # else:
        #     print("\nback in loc_var_wr after executing task!\n")
        # print("\n\nHERE in loc_var_wr!\n\n")
        self.mode = 'EXECUTING'
        (res, _, _) = self.ret

        environment[id] = res['val']
        self.ret = (res, environment, state_vars)


    """
    IMPORTANT NOTE
    """
    # NOTE: these have yet to be implemented
        # the equivalent of function invocation
    def e_task_invocation(self, instr, environment, state_vars):
        pass

        # native python function invocation (interface with agent/environment)
    def e_action_invocation(self, instr, environment, state_vars):
        pass

def dump(obj, nested_level=0, header=""):
    spacing = '   '
    string = header

    if type(obj) == dict:
        string = string + '%s{' % ((nested_level) * spacing) + '\n'
        for k, v in obj.items():
            if k == '__builtins__':
                continue
            elif hasattr(v, '__iter__'):
                string = string + '%s%s:' % ((nested_level + 1) * spacing, k) + '\n'
                string = string + dump(v, nested_level + 1) + '\n'
            else:
                string = string + '%s%s: %s' % ((nested_level + 1) * spacing, k, v) + '\n'
        string = string + '%s}' % (nested_level * spacing) + '\n'
    elif type(obj) == list:
        string = string + '%s[' % ((nested_level) * spacing) + '\n'
        for v in obj:
            if hasattr(v, '__iter__'):
                string = string + dump(v, nested_level + 1) + '\n'
            else:
                string = string + '%s%s' % ((nested_level + 1) * spacing, v) + '\n'
        string = string + '%s]' % ((nested_level) * spacing) + '\n'
    else:
        string = string + '%s%s' % (nested_level * spacing, obj) + '\n'

    return string


"""
TOP-LEVEL CODE

By convention, we'll put top-level code here, at the bottom of the file (and
we'll use such code for debugging purposes, since this file is intended to
function as a module).
"""

# dom_lexer.print_token_stream("../domains/simple_domain/simple_domain.dom")
# meth_parser.print_asts("../domains/test_domain1/test_domain1.meth", \
#                        paged = False, debug=False)
