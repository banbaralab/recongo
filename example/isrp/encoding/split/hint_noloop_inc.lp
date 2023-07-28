%%% Hint: No loop
%%%
%%% @author Nagoya university ASP team
%%% @mail yuya.yamada@nagoya-u.jp
%%% @mail banbara@nagoya-u.jp

#program step(t).

:-     in(X,t):     in(X,T);
   not in(X,t): not in(X,T), node(X);
   T = 0..t-1 ; t > 0.
