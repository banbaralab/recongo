%%% Hint: Maximal IS
%%%
%%% @author Nagoya university ASP team
%%% @mail yuya.yamada@nagoya-u.jp
%%% @mail banbara@nagoya-u.jp

#program step(t).
% #const heumax = 10000.
#const heumax = 1000.

#heuristic in(Y,t): edge(X,Y), not in(X,t). [heumax-t,true]
#heuristic in(Y,t): edge(Y,X), not in(X,t). [heumax-t,true]


																						

