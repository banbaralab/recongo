%%% Hint: Distance constraints
%%%
%%% @author Nagoya university ASP team
%%% @mail yuya.yamada@nagoya-u.jp
%%% @mail banbara@nagoya-u.jp

#program step(t).

:- not { not in(X,T): goal(X) } t-T, T = 0..t, query(t).
%:- not { not in(X,T): goal(X) } t-T, T = 0..t-1, query(t).

