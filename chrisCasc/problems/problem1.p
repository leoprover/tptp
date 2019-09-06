%--------------------------------------------------------------------------
% File     : PLA003-1 : TPTP v7.0.0. Released v1.0.0.
% Domain   : Planning
% Problem  : Monkey and Bananas Problem
% Version  : Especial.
% English  :

% Refs     :
% Source   : [SPRFN]
% Names    :

% Status   : Unsatisfiable
% Rating   : 0.00 v5.3.0, 0.05 v5.2.0, 0.00 v2.2.1, 0.11 v2.1.0, 0.00 v2.0.0
% Syntax   : Number of clauses     :   11 (   0 non-Horn;   2 unit;   8 RR)
%            Number of atoms       :   20 (   0 equality)
%            Maximal clause size   :    2 (   2 average)
%            Number of predicates  :    1 (   0 propositional; 3-3 arity)
%            Number of functors    :   11 (   8 constant; 0-3 arity)
%            Number of variables   :   31 (   7 singleton)
%            Maximal term depth    :    2 (   2 average)
% SPC      : CNF_UNS_RFO_NEQ_HRN

% Comments : Formulated as a state space.
%--------------------------------------------------------------------------

thf(0,type,a:$o).
thf(1,conjecture,(a => a)).