%%% Hint: No double jumping
%%%
%%% @author Nagoya university ASP team
%%% @mail yuya.yamada@nagoya-u.jp
%%% @mail banbara@nagoya-u.jp

#program step(t).

:- token_added(X,t-1), not in(X,t), t > 1.
