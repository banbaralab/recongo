%%% Independent Set Reconfiguration (token jumping)
%%% basic version
%%%
%%% @author Nagoya university ASP team
%%% @mail yuya.yamada@nagoya-u.jp
%%% @mail banbara@nagoya-u.jp

#program base.

% start configuration
:- not in(X,0), start(X).

#program step(t).

% independent set constraints
K { in(X,t): node(X) } K :- k(K).
:- in(X,t), in(Y,t), edge(X,Y).

% transition constraints (exact-one)
token_added(X,t) :- not in(X,t-1), in(X,t), t > 0.
:- not 1 { token_added(X,t) } 1, t > 0.

#program check(t).

% goal configuration
:- not in(X,t), goal(X), query(t).
