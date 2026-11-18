(function(){
var t=document.querySelector('.menu-toggle'),n=document.getElementById('site-nav');
if(t&&n)t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');});
var p=new URLSearchParams(location.search);
var qp=document.getElementById('qpart');if(qp&&p.get('part'))qp.value=p.get('part');
var f=document.getElementById('qf');
if(f)f.addEventListener('submit',function(ev){ev.preventDefault();var d=new FormData(f);
 var b='Name: '+d.get('name')+'\nEmail: '+d.get('email')+'\nPhone: '+d.get('phone')+'\nPart / brand / qty: '+d.get('part')+'\n\n'+d.get('msg');
 location.href='mailto:'+f.dataset.to+'?subject='+encodeURIComponent('Quote request from '+d.get('name'))+'&body='+encodeURIComponent(b);});
var sr=document.getElementById('sr');
if(sr&&window.GTA_INDEX){var q=(p.get('q')||'').toLowerCase().trim();
 document.getElementById('st').textContent='Search: \u201c'+(p.get('q')||'')+'\u201d';
 var r=window.GTA_INDEX.filter(function(i){return q&&(i.t+' '+i.no+' '+i.d+' '+i.s).toLowerCase().indexOf(q)>-1;});
 document.getElementById('sc').textContent=r.length+' results';
 sr.innerHTML=r.length?r.map(function(i){var a=document.createElement('a');return '<div class="cbox"><b>Part #'+i.no+'</b> &mdash; <a href="../'+i.u+'" style="color:#e4173a">'+i.t.replace(/</g,'&lt;')+'</a><br><small>'+i.s+'</small><p>'+i.d.replace(/</g,'&lt;')+'</p></div>';}).join(''):'<div class="cbox">No parts matched. Call us and we will source it.</div>';}
})();