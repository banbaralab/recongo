%%% Hint: Distance constraints
%%%
%%% @author Nagoya university ASP team
%%% @mail yuya.yamada@nagoya-u.jp
%%% @mail banbara@nagoya-u.jp

#program step(t).

:- not { not in(X,t): start(X) } t.
