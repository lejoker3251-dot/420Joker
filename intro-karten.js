/* 420 Joker: Intro mit vielen schwebenden Karten.
   Einbinden: <script src="intro-karten.js"></script> direkt unter <div id="intro" ...> in index.html */
(function(){
  var d=document,iv=d.getElementById("intro");
  if(!iv||matchMedia("(prefers-reduced-motion:reduce)").matches)return;
  var css=
"#intro .full{z-index:20;animation:reveal 2.2s 1.5s cubic-bezier(.2,.6,.2,1) both}"+
"#intro small{z-index:21}"+
"#intro .fc{position:absolute;left:var(--x);top:0;width:var(--w);aspect-ratio:2/3;border-radius:8%;"+
"background:var(--img) center/cover no-repeat;box-shadow:0 10px 40px rgba(150,70,255,.4);"+
"opacity:0;filter:blur(var(--b));will-change:transform,opacity;pointer-events:none;"+
"animation:fcIn var(--t) var(--d) cubic-bezier(.2,.7,.2,1) both}"+
"@keyframes fcIn{"+
"0%{opacity:0;transform:translate3d(0,calc(var(--y) + 14vh),0) rotate(var(--r0)) scale(.7)}"+
"28%{opacity:var(--o)}"+
"100%{opacity:var(--o);transform:translate3d(var(--dx),calc(var(--y) - 22vh),0) rotate(var(--r1)) scale(1)}}";
  var st=d.createElement("style");st.textContent=css;d.head.appendChild(st);

  /* Eure Karten: Joker in Lila kommt doppelt vor, damit er öfter erscheint */
  var imgs=["karte-lila-klein.webp","karte-rot-klein.webp","karte-dame-lila-klein.webp","karte-rot2-klein.webp","karte-lila-klein.webp"];
  var m=innerWidth<600,n=m?16:30,f=d.createDocumentFragment(),full=iv.querySelector(".full");
  function R(a,b){return a+Math.random()*(b-a)}
  for(var k=0;k<n;k++){
    var z=Math.random(),e=d.createElement("i");
    e.className="fc";
    e.style.cssText=
      "--img:url("+imgs[k%imgs.length]+");"+
      "--x:"+R(-4,92).toFixed(1)+"%;"+
      "--y:"+R(4,70).toFixed(1)+"vh;"+
      "--w:"+Math.round(54+z*(m?72:120))+"px;"+
      "--b:"+(z>.88?"3px":"0px")+";"+
      "--o:"+(.45+z*.55).toFixed(2)+";"+
      "--t:"+R(2.6,3.4).toFixed(2)+"s;"+
      "--d:"+R(0,.9).toFixed(2)+"s;"+
      "--r0:"+Math.round(R(-35,35))+"deg;"+
      "--r1:"+Math.round(R(-70,70))+"deg;"+
      "--dx:"+Math.round(R(-70,70))+"px;"+
      "z-index:"+Math.round(z*10);
    f.appendChild(e);
  }
  iv.insertBefore(f,full);
})();
