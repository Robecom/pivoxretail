(function(){
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
var h=document.querySelector('header');
addEventListener('scroll',function(){h.classList.toggle('scrolled',scrollY>8)},{passive:true});
if(!reduce&&'IntersectionObserver' in window){
  var els=document.querySelectorAll('.sec h2,.tile,.card,.vals div,.strip a');
  els.forEach(function(e,i){e.classList.add('rv');e.style.setProperty('--d',(i%5)*70+'ms')});
  var io=new IntersectionObserver(function(es){es.forEach(function(x){if(!x.isIntersecting)return;var t=x.target;t.classList.add('in');io.unobserve(t);setTimeout(function(){t.classList.remove('rv','in')},1100)})},{threshold:.1});
  els.forEach(function(e){io.observe(e)});
}
var root=document.getElementById('catalog');if(!root)return;
var SH=['jar','bottle','can','bag','box','sack','bar'],COL={pantry:'#E8E2D6',sauces:'#EBD3BE',snacks:'#F0D9D2',beverages:'#D3E0E4',grains:'#DCE4CF'},PAGE=48,email=root.dataset.email;
var grid=document.getElementById('grid'),more=document.getElementById('more'),count=document.getElementById('count'),q=document.getElementById('q'),sel=document.getElementById('brand'),chips=[].slice.call(root.querySelectorAll('.chips button'));
var all=[],view=[],shown=0,st={c:'all',b:'',q:''};
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/'/g,'&#39;').replace(/"/g,'&quot;')}
function card(p){
  var pic=p.m?"<div class='pic photo'><img src='/images/products/"+esc(p.m)+"' alt='"+esc(p.b+' '+p.n)+"' loading='lazy'></div>":"<div class='pic' style='--c:"+COL[p.c]+"'><svg viewBox='0 0 240 240' aria-hidden='true'><use href='/sprites.svg#"+SH[p.h]+"-"+p.k+"'/></svg></div>";
  var href='/product/'+p.u+'.html';
  var mail='mailto:'+email+'?subject='+encodeURIComponent('Inquiry: '+p.b+' '+p.n+' ('+p.u+')');
  return "<article class='card pop' data-cat='"+p.c+"'><a class='pic-link' href='"+href+"' tabindex='-1' aria-hidden='true'>"+pic+"</a><div class='info'><p class='brand'>"+esc(p.b)+"</p><h3><a href='"+href+"'>"+esc(p.n)+"</a></h3><p class='size'>"+esc(p.s)+"</p><span class='price'>$"+p.p.toFixed(2)+"</span><a class='ask' href='"+mail+"'>Ask about availability</a></div></article>";
}
function label(){count.textContent=view.length?view.length.toLocaleString()+' products':'No products match. Try another search, or email us and we will help.'}
function draw(reset){
  if(reset){grid.innerHTML='';shown=0}
  grid.insertAdjacentHTML('beforeend',view.slice(shown,shown+PAGE).map(card).join(''));
  shown=Math.min(shown+PAGE,view.length);more.hidden=shown>=view.length;label();
}
function apply(){
  var t=st.q.trim().toLowerCase();
  view=all.filter(function(p){return(st.c==='all'||p.c===st.c)&&(!st.b||p.b===st.b)&&(!t||(p.b+' '+p.n+' '+p.u).toLowerCase().indexOf(t)>-1)});
  draw(true);
}
chips.forEach(function(b){b.addEventListener('click',function(){st.c=b.dataset.f;chips.forEach(function(c){c.setAttribute('aria-pressed',c===b)});apply()})});
var tm;q.addEventListener('input',function(){clearTimeout(tm);tm=setTimeout(function(){st.q=q.value;apply()},150)});
sel.addEventListener('change',function(){st.b=sel.value;apply()});
more.addEventListener('click',function(){draw(false)});
fetch('/products.json').then(function(r){return r.json()}).then(function(d){
  all=d;var u=new URLSearchParams(location.search),b=u.get('brand'),c=u.get('cat')||location.hash.slice(1);
  if(c&&COL[c]){st.c=c;chips.forEach(function(x){x.setAttribute('aria-pressed',x.dataset.f===c)})}
  if(b){st.b=b;sel.value=b}var q0=u.get('q');if(q0){st.q=q0;q.value=q0}
  if(st.c==='all'&&!st.b&&!st.q){view=all;shown=Math.min(PAGE,all.length);more.hidden=shown>=view.length;label()}else apply();
}).catch(function(){count.textContent='The catalog could not be loaded. Please email us.'});
})();
