
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftANDORleftEQUALSleftNOTleftLTGTLTEGTEleftPLUSMINUSleftTIMESDIVIDED_BYTHEN ELSIF DO WHILE TRUE MINUS GTE PRE TASK RPAREN LTE DIVIDED_BY PLUS LT COLON COMMA ASSIGN BODY GT END STRING EQUALS ELSE LPAREN TIMES ID IF AND FALSE INT FLOAT NOT ORstart : methodsmethods : method methods\n               |               method : ID LPAREN params RPAREN COLON task pre bodyparams : ID COMMA params\n              | ID\n              |             task : TASK COLON ID LPAREN params RPARENpre : PRE COLON preconditionspreconditions : bexpr AND preconditions\n                     | bexpr\n                     |                        body : BODY COLON exprsexprs : LPAREN exprs RPAREN\n             | expr exprs\n             |                    expr : LPAREN expr RPAREN\n            | control_structure\n            | bexpr\n            | aexpr\n            | string\n            | state_var_rd\n            | state_var_wr\n            | loc_var_rd\n            | loc_var_wr        control_structure : while_loop\n                         | if_statementwhile_loop : WHILE bexpr DO exprs ENDif_statement : IF bexpr THEN exprs END\n                    | IF bexpr THEN exprs elsif_blocks END\n                    | IF bexpr THEN exprs ELSE exprs END\n                    | IF bexpr THEN exprs elsif_blocks ELSE exprs ENDelsif_blocks : elsif_blocks elsif_block\n                    | elsif_block             elsif_block : ELSIF bexpr THEN exprsaexpr : aexpr PLUS aexpr\n             | aexpr MINUS aexpr\n             | aexpr TIMES aexpr\n             | aexpr DIVIDED_BY aexpr\n             | INT\n             | FLOAT\n             | ID                    bexpr : bexpr AND bexpr\n             | bexpr OR bexpr\n             | expr EQUALS expr\n             | expr LT expr\n             | expr GT expr\n             | expr LTE expr\n             | expr GTE expr\n             | NOT bexpr\n             | true\n             | false\n             | state_var_rd     true : TRUEfalse : FALSEstring : STRINGstate_var_rd : ID LPAREN state_var_args RPARENstate_var_wr : ID LPAREN state_var_args RPAREN ASSIGN exprstate_var_args : state_var_arg COMMA state_var_args\n                      | state_var_argstate_var_arg : state_var_rd\n                     | IDloc_var_rd : IDloc_var_wr : ID ASSIGN expr'
    
_lr_action_items = {'THEN':([23,24,25,26,27,29,30,31,32,33,34,35,38,41,42,44,49,50,51,63,70,76,77,78,79,80,83,84,89,91,92,93,94,95,99,101,108,113,115,116,117,123,125,],[-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,-51,-55,-40,-41,-22,-19,-42,90,-50,-42,-39,-38,-36,-37,-44,-17,-64,-47,-49,-45,-46,-48,-43,-57,-29,-28,-58,121,-30,-31,-32,]),'LPAREN':([4,20,21,22,23,24,25,26,27,29,30,31,32,33,34,35,37,38,39,40,41,42,44,45,46,48,49,50,51,52,58,59,62,64,65,66,67,68,70,72,74,76,77,78,79,80,83,84,85,89,90,91,92,93,94,95,96,99,101,106,108,109,111,113,115,117,118,121,123,125,],[6,37,47,48,-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,37,-51,61,37,-55,-40,-41,37,37,48,-22,-19,61,48,37,37,37,37,37,37,37,37,-50,48,37,-42,-39,-38,-36,-37,-44,-17,100,-64,48,-47,-49,-45,-46,-48,48,-43,-57,37,-29,37,48,-28,-58,-30,48,48,-31,-32,]),'DO':([23,24,25,26,27,29,30,31,32,33,34,35,38,41,42,44,49,50,51,69,70,76,77,78,79,80,83,84,89,91,92,93,94,95,99,101,108,113,115,117,123,125,],[-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,-51,-55,-40,-41,-22,-19,-42,96,-50,-42,-39,-38,-36,-37,-44,-17,-64,-47,-49,-45,-46,-48,-43,-57,-29,-28,-58,-30,-31,-32,]),'WHILE':([20,22,23,24,25,26,27,29,30,31,32,33,34,35,37,38,40,41,42,44,45,46,48,49,50,51,52,58,59,62,64,65,66,67,68,70,72,74,76,77,78,79,80,83,84,89,90,91,92,93,94,95,96,99,101,106,108,109,111,113,115,117,118,121,123,125,],[45,45,-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,45,-51,45,-55,-40,-41,45,45,45,-22,-19,-42,45,45,45,45,45,45,45,45,45,-50,45,45,-42,-39,-38,-36,-37,-44,-17,-64,45,-47,-49,-45,-46,-48,45,-43,-57,45,-29,45,45,-28,-58,-30,45,45,-31,-32,]),'TRUE':([20,22,23,24,25,26,27,29,30,31,32,33,34,35,37,38,40,41,42,44,45,46,48,49,50,51,52,58,59,62,64,65,66,67,68,70,72,74,76,77,78,79,80,83,84,89,90,91,92,93,94,95,96,99,101,106,108,109,111,113,115,117,118,121,123,125,],[30,30,-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,30,-51,30,-55,-40,-41,30,30,30,-22,-19,-42,30,30,30,30,30,30,30,30,30,-50,30,30,-42,-39,-38,-36,-37,-44,-17,-64,30,-47,-49,-45,-46,-48,30,-43,-57,30,-29,30,30,-28,-58,-30,30,30,-31,-32,]),'MINUS':([27,39,42,44,51,76,77,78,79,80,],[57,-42,-40,-41,-42,-42,-39,-38,-36,-37,]),'GTE':([23,24,25,26,27,28,29,30,31,32,33,34,35,38,39,41,42,43,44,49,50,51,52,60,63,69,70,72,76,77,78,79,80,81,83,84,89,91,92,93,94,95,99,101,108,113,115,116,117,123,125,],[-52,-22,-25,-18,-20,-19,-21,-54,-56,-27,-26,-23,-24,-51,-42,-55,-40,65,-41,-22,-19,-42,65,65,-19,-19,-19,65,-42,-39,-38,-36,-37,-19,-19,-17,65,-47,-49,65,-46,-48,-19,-57,-29,-28,65,-19,-30,-31,-32,]),'PRE':([13,97,],[16,-8,]),'TASK':([11,],[14,]),'RPAREN':([6,7,8,10,12,23,24,25,26,27,29,30,31,32,33,34,35,38,41,42,44,47,48,49,50,51,52,60,70,71,72,73,75,76,77,78,79,80,83,84,85,86,87,88,89,91,92,93,94,95,98,99,101,105,107,108,113,114,115,117,123,125,],[-7,9,-6,-7,-5,-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,-51,-55,-40,-41,-7,-16,-22,-19,-42,-16,84,-50,97,84,98,-15,-42,-39,-38,-36,-37,-44,-17,-62,-61,101,-60,-64,-47,-49,-45,-46,-48,-14,-43,-57,114,-59,-29,-28,-57,-58,-30,-31,-32,]),'DIVIDED_BY':([27,39,42,44,51,76,77,78,79,80,],[54,-42,-40,-41,-42,-42,-39,-38,54,54,]),'PLUS':([27,39,42,44,51,76,77,78,79,80,],[56,-42,-40,-41,-42,-42,-39,-38,-36,-37,]),'LT':([23,24,25,26,27,28,29,30,31,32,33,34,35,38,39,41,42,43,44,49,50,51,52,60,63,69,70,72,76,77,78,79,80,81,83,84,89,91,92,93,94,95,99,101,108,113,115,116,117,123,125,],[-52,-22,-25,-18,-20,-19,-21,-54,-56,-27,-26,-23,-24,-51,-42,-55,-40,67,-41,-22,-19,-42,67,67,-19,-19,-19,67,-42,-39,-38,-36,-37,-19,-19,-17,67,-47,-49,67,-46,-48,-19,-57,-29,-28,67,-19,-30,-31,-32,]),'COMMA':([8,85,86,88,114,],[10,-62,-61,102,-57,]),'COLON':([9,14,16,19,],[11,17,20,22,]),'ASSIGN':([39,51,101,],[62,62,106,]),'$end':([0,1,2,3,5,18,22,23,24,25,26,27,29,30,31,32,33,34,35,38,41,42,44,49,50,51,52,53,70,75,76,77,78,79,80,83,84,89,91,92,93,94,95,98,99,101,108,113,115,117,123,125,],[-3,-1,-3,0,-2,-4,-16,-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,-51,-55,-40,-41,-22,-19,-42,-16,-13,-50,-15,-42,-39,-38,-36,-37,-44,-17,-64,-47,-49,-45,-46,-48,-14,-43,-57,-29,-28,-58,-30,-31,-32,]),'BODY':([15,20,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,41,42,44,49,50,51,58,70,76,77,78,79,80,81,82,83,84,89,91,92,93,94,95,99,101,108,113,115,117,123,125,],[19,-12,-52,-53,-25,-18,-20,-11,-21,-54,-56,-27,-26,-23,-24,-9,-51,-55,-40,-41,-22,-19,-42,-12,-50,-42,-39,-38,-36,-37,-11,-10,-44,-17,-64,-47,-49,-45,-46,-48,-43,-57,-29,-28,-58,-30,-31,-32,]),'GT':([23,24,25,26,27,28,29,30,31,32,33,34,35,38,39,41,42,43,44,49,50,51,52,60,63,69,70,72,76,77,78,79,80,81,83,84,89,91,92,93,94,95,99,101,108,113,115,116,117,123,125,],[-52,-22,-25,-18,-20,-19,-21,-54,-56,-27,-26,-23,-24,-51,-42,-55,-40,64,-41,-22,-19,-42,64,64,-19,-19,-19,64,-42,-39,-38,-36,-37,-19,-19,-17,64,-47,-49,64,-46,-48,-19,-57,-29,-28,64,-19,-30,-31,-32,]),'END':([23,24,25,26,27,29,30,31,32,33,34,35,38,41,42,44,49,50,51,52,70,75,76,77,78,79,80,83,84,89,90,91,92,93,94,95,96,98,99,101,103,104,108,110,111,112,113,115,117,118,119,120,121,122,123,124,125,],[-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,-51,-55,-40,-41,-22,-19,-42,-16,-50,-15,-42,-39,-38,-36,-37,-44,-17,-64,-16,-47,-49,-45,-46,-48,-16,-14,-43,-57,108,113,-29,117,-16,-34,-28,-58,-30,-16,-33,123,-16,125,-31,-35,-32,]),'STRING':([20,22,23,24,25,26,27,29,30,31,32,33,34,35,37,38,40,41,42,44,45,46,48,49,50,51,52,58,59,62,64,65,66,67,68,70,72,74,76,77,78,79,80,83,84,89,90,91,92,93,94,95,96,99,101,106,108,109,111,113,115,117,118,121,123,125,],[31,31,-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,31,-51,31,-55,-40,-41,31,31,31,-22,-19,-42,31,31,31,31,31,31,31,31,31,-50,31,31,-42,-39,-38,-36,-37,-44,-17,-64,31,-47,-49,-45,-46,-48,31,-43,-57,31,-29,31,31,-28,-58,-30,31,31,-31,-32,]),'EQUALS':([23,24,25,26,27,28,29,30,31,32,33,34,35,38,39,41,42,43,44,49,50,51,52,60,63,69,70,72,76,77,78,79,80,81,83,84,89,91,92,93,94,95,99,101,108,113,115,116,117,123,125,],[-52,-22,-25,-18,-20,-19,-21,-54,-56,-27,-26,-23,-24,-51,-42,-55,-40,66,-41,-22,-19,-42,66,66,-19,-19,-19,66,-42,-39,-38,-36,-37,-19,-19,-17,66,-47,-49,-45,-46,-48,-19,-57,-29,-28,66,-19,-30,-31,-32,]),'ELSE':([23,24,25,26,27,29,30,31,32,33,34,35,38,41,42,44,49,50,51,52,70,75,76,77,78,79,80,83,84,89,90,91,92,93,94,95,98,99,101,103,108,110,112,113,115,117,119,121,123,124,125,],[-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,-51,-55,-40,-41,-22,-19,-42,-16,-50,-15,-42,-39,-38,-36,-37,-44,-17,-64,-16,-47,-49,-45,-46,-48,-14,-43,-57,111,-29,118,-34,-28,-58,-30,-33,-16,-31,-35,-32,]),'LTE':([23,24,25,26,27,28,29,30,31,32,33,34,35,38,39,41,42,43,44,49,50,51,52,60,63,69,70,72,76,77,78,79,80,81,83,84,89,91,92,93,94,95,99,101,108,113,115,116,117,123,125,],[-52,-22,-25,-18,-20,-19,-21,-54,-56,-27,-26,-23,-24,-51,-42,-55,-40,68,-41,-22,-19,-42,68,68,-19,-19,-19,68,-42,-39,-38,-36,-37,-19,-19,-17,68,-47,-49,68,-46,-48,-19,-57,-29,-28,68,-19,-30,-31,-32,]),'TIMES':([27,39,42,44,51,76,77,78,79,80,],[55,-42,-40,-41,-42,-42,-39,-38,55,55,]),'ID':([0,2,6,10,17,18,20,22,23,24,25,26,27,29,30,31,32,33,34,35,37,38,40,41,42,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,61,62,64,65,66,67,68,70,72,74,75,76,77,78,79,80,83,84,89,90,91,92,93,94,95,96,98,99,100,101,102,106,108,109,111,113,115,117,118,121,123,125,],[4,4,8,8,21,-4,39,51,-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,51,-51,39,-55,-40,-41,39,39,8,51,-22,-19,-42,51,-13,76,76,76,76,39,39,85,51,51,51,51,51,51,-50,51,39,-15,-42,-39,-38,-36,-37,-44,-17,-64,51,-47,-49,-45,-46,-48,51,-14,-43,85,-57,85,51,-29,39,51,-28,-58,-30,51,51,-31,-32,]),'IF':([20,22,23,24,25,26,27,29,30,31,32,33,34,35,37,38,40,41,42,44,45,46,48,49,50,51,52,58,59,62,64,65,66,67,68,70,72,74,76,77,78,79,80,83,84,89,90,91,92,93,94,95,96,99,101,106,108,109,111,113,115,117,118,121,123,125,],[40,40,-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,40,-51,40,-55,-40,-41,40,40,40,-22,-19,-42,40,40,40,40,40,40,40,40,40,-50,40,40,-42,-39,-38,-36,-37,-44,-17,-64,40,-47,-49,-45,-46,-48,40,-43,-57,40,-29,40,40,-28,-58,-30,40,40,-31,-32,]),'AND':([23,24,25,26,27,28,29,30,31,32,33,34,35,38,41,42,44,49,50,51,63,69,70,76,77,78,79,80,81,83,84,89,91,92,93,94,95,99,101,108,113,115,116,117,123,125,],[-52,-53,-25,-18,-20,58,-21,-54,-56,-27,-26,-23,-24,-51,-55,-40,-41,-22,74,-42,74,74,-50,-42,-39,-38,-36,-37,-43,-44,-17,-64,-47,-49,-45,-46,-48,-43,-57,-29,-28,-58,74,-30,-31,-32,]),'FALSE':([20,22,23,24,25,26,27,29,30,31,32,33,34,35,37,38,40,41,42,44,45,46,48,49,50,51,52,58,59,62,64,65,66,67,68,70,72,74,76,77,78,79,80,83,84,89,90,91,92,93,94,95,96,99,101,106,108,109,111,113,115,117,118,121,123,125,],[41,41,-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,41,-51,41,-55,-40,-41,41,41,41,-22,-19,-42,41,41,41,41,41,41,41,41,41,-50,41,41,-42,-39,-38,-36,-37,-44,-17,-64,41,-47,-49,-45,-46,-48,41,-43,-57,41,-29,41,41,-28,-58,-30,41,41,-31,-32,]),'INT':([20,22,23,24,25,26,27,29,30,31,32,33,34,35,37,38,40,41,42,44,45,46,48,49,50,51,52,54,55,56,57,58,59,62,64,65,66,67,68,70,72,74,76,77,78,79,80,83,84,89,90,91,92,93,94,95,96,99,101,106,108,109,111,113,115,117,118,121,123,125,],[42,42,-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,42,-51,42,-55,-40,-41,42,42,42,-22,-19,-42,42,42,42,42,42,42,42,42,42,42,42,42,42,-50,42,42,-42,-39,-38,-36,-37,-44,-17,-64,42,-47,-49,-45,-46,-48,42,-43,-57,42,-29,42,42,-28,-58,-30,42,42,-31,-32,]),'FLOAT':([20,22,23,24,25,26,27,29,30,31,32,33,34,35,37,38,40,41,42,44,45,46,48,49,50,51,52,54,55,56,57,58,59,62,64,65,66,67,68,70,72,74,76,77,78,79,80,83,84,89,90,91,92,93,94,95,96,99,101,106,108,109,111,113,115,117,118,121,123,125,],[44,44,-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,44,-51,44,-55,-40,-41,44,44,44,-22,-19,-42,44,44,44,44,44,44,44,44,44,44,44,44,44,-50,44,44,-42,-39,-38,-36,-37,-44,-17,-64,44,-47,-49,-45,-46,-48,44,-43,-57,44,-29,44,44,-28,-58,-30,44,44,-31,-32,]),'ELSIF':([23,24,25,26,27,29,30,31,32,33,34,35,38,41,42,44,49,50,51,52,70,75,76,77,78,79,80,83,84,89,90,91,92,93,94,95,98,99,101,103,108,110,112,113,115,117,119,121,123,124,125,],[-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,-51,-55,-40,-41,-22,-19,-42,-16,-50,-15,-42,-39,-38,-36,-37,-44,-17,-64,-16,-47,-49,-45,-46,-48,-14,-43,-57,109,-29,109,-34,-28,-58,-30,-33,-16,-31,-35,-32,]),'NOT':([20,22,23,24,25,26,27,29,30,31,32,33,34,35,37,38,40,41,42,44,45,46,48,49,50,51,52,58,59,62,64,65,66,67,68,70,72,74,76,77,78,79,80,83,84,89,90,91,92,93,94,95,96,99,101,106,108,109,111,113,115,117,118,121,123,125,],[46,46,-52,-53,-25,-18,-20,-21,-54,-56,-27,-26,-23,-24,46,-51,46,-55,-40,-41,46,46,46,-22,-19,-42,46,46,46,46,46,46,46,46,46,-50,46,46,-42,-39,-38,-36,-37,-44,-17,-64,46,-47,-49,-45,-46,-48,46,-43,-57,46,-29,46,46,-28,-58,-30,46,46,-31,-32,]),'OR':([23,24,25,26,27,28,29,30,31,32,33,34,35,38,41,42,44,49,50,51,63,69,70,76,77,78,79,80,81,83,84,89,91,92,93,94,95,99,101,108,113,115,116,117,123,125,],[-52,-53,-25,-18,-20,59,-21,-54,-56,-27,-26,-23,-24,-51,-55,-40,-41,-22,59,-42,59,59,-50,-42,-39,-38,-36,-37,-43,-44,-17,-64,-47,-49,-45,-46,-48,-43,-57,-29,-28,-58,59,-30,-31,-32,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'pre':([13,],[15,]),'false':([20,22,37,40,45,46,48,52,58,59,62,64,65,66,67,68,72,74,90,96,106,109,111,118,121,],[23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,]),'methods':([0,2,],[1,5,]),'elsif_blocks':([103,],[110,]),'state_var_rd':([20,22,37,40,45,46,48,52,58,59,61,62,64,65,66,67,68,72,74,90,96,100,102,106,109,111,118,121,],[24,49,49,24,24,24,49,49,24,24,86,49,49,49,49,49,49,49,24,49,49,86,86,49,24,49,49,49,]),'state_var_args':([61,100,102,],[87,105,107,]),'loc_var_wr':([20,22,37,40,45,46,48,52,58,59,62,64,65,66,67,68,72,74,90,96,106,109,111,118,121,],[25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,]),'control_structure':([20,22,37,40,45,46,48,52,58,59,62,64,65,66,67,68,72,74,90,96,106,109,111,118,121,],[26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,]),'aexpr':([20,22,37,40,45,46,48,52,54,55,56,57,58,59,62,64,65,66,67,68,72,74,90,96,106,109,111,118,121,],[27,27,27,27,27,27,27,27,77,78,79,80,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,]),'bexpr':([20,22,37,40,45,46,48,52,58,59,62,64,65,66,67,68,72,74,90,96,106,109,111,118,121,],[28,50,50,63,69,70,50,50,81,83,50,50,50,50,50,50,50,99,50,50,50,116,50,50,50,]),'start':([0,],[3,]),'params':([6,10,47,],[7,12,71,]),'elsif_block':([103,110,],[112,119,]),'if_statement':([20,22,37,40,45,46,48,52,58,59,62,64,65,66,67,68,72,74,90,96,106,109,111,118,121,],[32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,]),'method':([0,2,],[2,2,]),'body':([15,],[18,]),'string':([20,22,37,40,45,46,48,52,58,59,62,64,65,66,67,68,72,74,90,96,106,109,111,118,121,],[29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,]),'while_loop':([20,22,37,40,45,46,48,52,58,59,62,64,65,66,67,68,72,74,90,96,106,109,111,118,121,],[33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,]),'state_var_wr':([20,22,37,40,45,46,48,52,58,59,62,64,65,66,67,68,72,74,90,96,106,109,111,118,121,],[34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,]),'loc_var_rd':([20,22,37,40,45,46,48,52,58,59,62,64,65,66,67,68,72,74,90,96,106,109,111,118,121,],[35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,35,]),'preconditions':([20,58,],[36,82,]),'true':([20,22,37,40,45,46,48,52,58,59,62,64,65,66,67,68,72,74,90,96,106,109,111,118,121,],[38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,]),'task':([11,],[13,]),'expr':([20,22,37,40,45,46,48,52,58,59,62,64,65,66,67,68,72,74,90,96,106,109,111,118,121,],[43,52,60,43,43,43,72,52,43,43,89,91,92,93,94,95,52,43,52,52,115,43,52,52,52,]),'exprs':([22,48,52,72,90,96,111,118,121,],[53,73,75,75,103,104,120,122,124,]),'state_var_arg':([61,100,102,],[88,88,88,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> methods','start',1,'p_start','meth_parser.py',167),
  ('methods -> method methods','methods',2,'p_methods','meth_parser.py',172),
  ('methods -> <empty>','methods',0,'p_methods','meth_parser.py',173),
  ('method -> ID LPAREN params RPAREN COLON task pre body','method',8,'p_method','meth_parser.py',191),
  ('params -> ID COMMA params','params',3,'p_params','meth_parser.py',207),
  ('params -> ID','params',1,'p_params','meth_parser.py',208),
  ('params -> <empty>','params',0,'p_params','meth_parser.py',209),
  ('task -> TASK COLON ID LPAREN params RPAREN','task',6,'p_task','meth_parser.py',223),
  ('pre -> PRE COLON preconditions','pre',3,'p_pre','meth_parser.py',238),
  ('preconditions -> bexpr AND preconditions','preconditions',3,'p_precon_list','meth_parser.py',245),
  ('preconditions -> bexpr','preconditions',1,'p_precon_list','meth_parser.py',246),
  ('preconditions -> <empty>','preconditions',0,'p_precon_list','meth_parser.py',247),
  ('body -> BODY COLON exprs','body',3,'p_body','meth_parser.py',261),
  ('exprs -> LPAREN exprs RPAREN','exprs',3,'p_exprs','meth_parser.py',273),
  ('exprs -> expr exprs','exprs',2,'p_exprs','meth_parser.py',274),
  ('exprs -> <empty>','exprs',0,'p_exprs','meth_parser.py',275),
  ('expr -> LPAREN expr RPAREN','expr',3,'p_expr','meth_parser.py',294),
  ('expr -> control_structure','expr',1,'p_expr','meth_parser.py',295),
  ('expr -> bexpr','expr',1,'p_expr','meth_parser.py',296),
  ('expr -> aexpr','expr',1,'p_expr','meth_parser.py',297),
  ('expr -> string','expr',1,'p_expr','meth_parser.py',298),
  ('expr -> state_var_rd','expr',1,'p_expr','meth_parser.py',299),
  ('expr -> state_var_wr','expr',1,'p_expr','meth_parser.py',300),
  ('expr -> loc_var_rd','expr',1,'p_expr','meth_parser.py',301),
  ('expr -> loc_var_wr','expr',1,'p_expr','meth_parser.py',302),
  ('control_structure -> while_loop','control_structure',1,'p_control_structure','meth_parser.py',311),
  ('control_structure -> if_statement','control_structure',1,'p_control_structure','meth_parser.py',312),
  ('while_loop -> WHILE bexpr DO exprs END','while_loop',5,'p_while_loop','meth_parser.py',316),
  ('if_statement -> IF bexpr THEN exprs END','if_statement',5,'p_if_statement','meth_parser.py',324),
  ('if_statement -> IF bexpr THEN exprs elsif_blocks END','if_statement',6,'p_if_statement','meth_parser.py',325),
  ('if_statement -> IF bexpr THEN exprs ELSE exprs END','if_statement',7,'p_if_statement','meth_parser.py',326),
  ('if_statement -> IF bexpr THEN exprs elsif_blocks ELSE exprs END','if_statement',8,'p_if_statement','meth_parser.py',327),
  ('elsif_blocks -> elsif_blocks elsif_block','elsif_blocks',2,'p_elsif_blocks','meth_parser.py',364),
  ('elsif_blocks -> elsif_block','elsif_blocks',1,'p_elsif_blocks','meth_parser.py',365),
  ('elsif_block -> ELSIF bexpr THEN exprs','elsif_block',4,'p_elsif_block','meth_parser.py',376),
  ('aexpr -> aexpr PLUS aexpr','aexpr',3,'p_aexpr','meth_parser.py',395),
  ('aexpr -> aexpr MINUS aexpr','aexpr',3,'p_aexpr','meth_parser.py',396),
  ('aexpr -> aexpr TIMES aexpr','aexpr',3,'p_aexpr','meth_parser.py',397),
  ('aexpr -> aexpr DIVIDED_BY aexpr','aexpr',3,'p_aexpr','meth_parser.py',398),
  ('aexpr -> INT','aexpr',1,'p_aexpr','meth_parser.py',399),
  ('aexpr -> FLOAT','aexpr',1,'p_aexpr','meth_parser.py',400),
  ('aexpr -> ID','aexpr',1,'p_aexpr','meth_parser.py',401),
  ('bexpr -> bexpr AND bexpr','bexpr',3,'p_bexpr','meth_parser.py',432),
  ('bexpr -> bexpr OR bexpr','bexpr',3,'p_bexpr','meth_parser.py',433),
  ('bexpr -> expr EQUALS expr','bexpr',3,'p_bexpr','meth_parser.py',434),
  ('bexpr -> expr LT expr','bexpr',3,'p_bexpr','meth_parser.py',435),
  ('bexpr -> expr GT expr','bexpr',3,'p_bexpr','meth_parser.py',436),
  ('bexpr -> expr LTE expr','bexpr',3,'p_bexpr','meth_parser.py',437),
  ('bexpr -> expr GTE expr','bexpr',3,'p_bexpr','meth_parser.py',438),
  ('bexpr -> NOT bexpr','bexpr',2,'p_bexpr','meth_parser.py',439),
  ('bexpr -> true','bexpr',1,'p_bexpr','meth_parser.py',440),
  ('bexpr -> false','bexpr',1,'p_bexpr','meth_parser.py',441),
  ('bexpr -> state_var_rd','bexpr',1,'p_bexpr','meth_parser.py',442),
  ('true -> TRUE','true',1,'p_true','meth_parser.py',467),
  ('false -> FALSE','false',1,'p_false','meth_parser.py',474),
  ('string -> STRING','string',1,'p_string','meth_parser.py',481),
  ('state_var_rd -> ID LPAREN state_var_args RPAREN','state_var_rd',4,'p_state_var_rd','meth_parser.py',491),
  ('state_var_wr -> ID LPAREN state_var_args RPAREN ASSIGN expr','state_var_wr',6,'p_state_var_wr','meth_parser.py',499),
  ('state_var_args -> state_var_arg COMMA state_var_args','state_var_args',3,'p_state_var_args','meth_parser.py',507),
  ('state_var_args -> state_var_arg','state_var_args',1,'p_state_var_args','meth_parser.py',508),
  ('state_var_arg -> state_var_rd','state_var_arg',1,'p_state_var_arg','meth_parser.py',515),
  ('state_var_arg -> ID','state_var_arg',1,'p_state_var_arg','meth_parser.py',516),
  ('loc_var_rd -> ID','loc_var_rd',1,'p_loc_var_rd','meth_parser.py',520),
  ('loc_var_wr -> ID ASSIGN expr','loc_var_wr',3,'p_loc_var_wr','meth_parser.py',527),
]
