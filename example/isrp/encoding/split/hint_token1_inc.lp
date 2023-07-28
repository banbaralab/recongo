%%% Hint: No one back
%%%
%%% @author Nagoya university ASP team
%%% @mail yuya.yamada@nagoya-u.jp
%%% @mail banbara@nagoya-u.jp

#program step(t).

token_removed(X,t) :- in(X,t-1), not in(X,t), t > 0.
:- token_removed(X,t-1), in(X,t), t > 1.
