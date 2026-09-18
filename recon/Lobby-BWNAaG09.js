import{r as v,a7 as Me,h as He,aa as qe,ab as Mt,j as c,Q as dn,ac as mn,ad as pn,ae as hn,F as X,af as gn,ag as yn,ah as vn,B as se,c as bn,ai as xn,aj as At,U as Rt,ak as Lt,al as kn,am as wn,an as Sn,ao as lt,ap as jn,aq as Cn,ar as Nn,as as In,t as Ae,at as En,au as Mn,av as An,aw as Rn,ax as Ln,ay as ie,az as _n,aA as Ke,aB as Je,aC as On,aD as Tn,T as $n,w as _t,J as Qe,aE as Ze,aF as Pn,aG as Dn,aH as zn,aI as Bn,aJ as Ot,aK as Fn,aL as Vn,L as Yn,aM as Un,aN as Xn,aO as Wn,aP as Gn,aQ as Hn,i as qn,aR as Kn,aS as Jn,a2 as Qn,aT as Zn,aU as er,aV as tr,aW as nr,aX as rr,aY as ar,aZ as sr,a_ as ir,a$ as or,b0 as cr,b1 as ur,b2 as lr,k as fr,b3 as dr,b4 as mr}from"../index.CvXZKfiM.js";import{a as pr,L as et,b as hr}from"./AnimatedFitHeight-DW7Ku1Uq.js";import{g as gr,P as yr,D as ft,R as vr,f as br,c as xr}from"./luxon-BJFF9-jg.js";import{g as kr,u as wr,S as Sr,r as jr,a as Cr,s as Nr}from"./Slider-CndKmlgR.js";import Ir from"./sad-tear-D0dI1rlN.js";import{S as Er}from"./StoreItemImage-B57S5zVh.js";import{u as Mr}from"./usePushNotifications-BWEoUDSJ.js";(function(){try{var e=typeof window<"u"?window:typeof global<"u"?global:typeof globalThis<"u"?globalThis:typeof self<"u"?self:{};e.SENTRY_RELEASE={id:"a5537d2c"},e._sentryModuleMetadata=e._sentryModuleMetadata||{},e._sentryModuleMetadata[new e.Error().stack]=(function(r){for(var a=1;a<arguments.length;a++){var i=arguments[a];if(i!=null)for(var s in i)i.hasOwnProperty(s)&&(r[s]=i[s])}return r})({},e._sentryModuleMetadata[new e.Error().stack],{"_sentryBundlerPluginAppKey:richup-frontend":!0});var t=new e.Error().stack;t&&(e._sentryDebugIds=e._sentryDebugIds||{},e._sentryDebugIds[t]="6485822c-6687-4545-ba73-b33d8bb2dc66",e._sentryDebugIdIdentifier="sentry-dbid-6485822c-6687-4545-ba73-b33d8bb2dc66")}catch{}})();function Ar(){const[e,t]=v.useState(void 0);return v.useEffect(()=>{function r(){return typeof document<"u"?document.documentElement.clientHeight:void 0}function a(){t(r())}return a(),window.addEventListener("resize",a),()=>window.removeEventListener("resize",a)},[]),e}const Rr="f-OECMum",Lr="Nh9KLIyH",_r="Wcde9SSR",Or="_4OA9nsIH",Tr="_3L8AzBAV",fe={container:Rr,nameContainer:Lr,input:_r,randomBtn:Or,userProfile:Tr};function $r({onNameUpdated:e}){const{name:t}=v.useContext(Me),r=He(),[a,i]=v.useState(t||qe(Mt,""));function s(o){i(o),e(o)}return v.useEffect(()=>{r.data?.name&&(a||s(r.data.name))},[r]),c.jsx("div",{className:fe.container,children:c.jsx(dn,{query:r,loadingComponent:c.jsx(vn,{}),children:o=>o?c.jsx(mn,{user:o,nameHint:"Playing as",className:fe.userProfile}):c.jsxs("div",{className:fe.nameContainer,children:[c.jsx(pn,{value:a,onChange:u=>s(u.target.value),placeholder:"Your nickname...",className:fe.input,maxLength:hn}),c.jsx("div",{className:fe.randomBtn,onClick:()=>s(yn()),children:c.jsx(X,{icon:gn})})]})})})}const Pr="AIJWZ5ob",Dr="TOibs0C6",zr="sbUwjYqM",Br="pAeeiDZs",Fr="xsw9wPme",Vr="MOpcbFmz",Yr="o6-VG5fr",Ur={gameLogo:Pr,logo:Dr,buttons:zr,whatsNew:Br,btn:Fr,aBtn:Vr,discord:Yr};function Xr({className:e,children:t,...r}){return c.jsx(se,{className:bn(Ur.btn,e),...r,children:t})}const Wr="jRRQ5s7R",Gr={popover:Wr};function Hr({className:e}){const[t,r]=Jr(),a=Kr(t),{dragGuardRef:i,onTooltipHideAttempt:s}=Qr(),o=()=>{r(u=>u===0?100:0)};return c.jsx(xn,{content:c.jsx(qr,{volume:t,setVolume:r,dragGuardRef:i}),theme:"richup-blended",interactive:!0,onHide:s,hideOnClick:!1,delay:[100,0],children:c.jsx(Xr,{className:e,onClick:o,children:c.jsx(X,{icon:a,size:"lg",fixedWidth:!0})})})}function qr({volume:e,setVolume:t,dragGuardRef:r}){return c.jsxs("div",{className:Gr.popover,children:[c.jsx(Sr,{value:e,min:0,max:100,onChange:t,includeDefaultMarks:!1,onBeforeChange:()=>{r.current=!0},onAfterChange:()=>{r.current=!1}}),c.jsxs("span",{children:[e,"%"]})]})}function Kr(e){return e===0?kn:e<=50?wn:Sn}function Jr(){const[e,t]=v.useState(0);return At(()=>{t(kr())}),Rt(()=>{e!==null&&wr(e)},[e]),[e,t]}function Qr(){const e=v.useRef(!1),t=v.useRef(void 0);Lt(()=>clearInterval(t.current));function r(a){if(e.current)return clearInterval(t.current),t.current=setInterval(()=>{e.current||(clearInterval(t.current),a.hide())},100),!1}return{dragGuardRef:e,onTooltipHideAttempt:r}}function Zr(e){if(e.sheet)return e.sheet;for(var t=0;t<document.styleSheets.length;t++)if(document.styleSheets[t].ownerNode===e)return document.styleSheets[t]}function ea(e){var t=document.createElement("style");return t.setAttribute("data-emotion",e.key),e.nonce!==void 0&&t.setAttribute("nonce",e.nonce),t.appendChild(document.createTextNode("")),t.setAttribute("data-s",""),t}var ta=(function(){function e(r){var a=this;this._insertTag=function(i){var s;a.tags.length===0?a.insertionPoint?s=a.insertionPoint.nextSibling:a.prepend?s=a.container.firstChild:s=a.before:s=a.tags[a.tags.length-1].nextSibling,a.container.insertBefore(i,s),a.tags.push(i)},this.isSpeedy=r.speedy===void 0?!0:r.speedy,this.tags=[],this.ctr=0,this.nonce=r.nonce,this.key=r.key,this.container=r.container,this.prepend=r.prepend,this.insertionPoint=r.insertionPoint,this.before=null}var t=e.prototype;return t.hydrate=function(a){a.forEach(this._insertTag)},t.insert=function(a){this.ctr%(this.isSpeedy?65e3:1)===0&&this._insertTag(ea(this));var i=this.tags[this.tags.length-1];if(this.isSpeedy){var s=Zr(i);try{s.insertRule(a,s.cssRules.length)}catch{}}else i.appendChild(document.createTextNode(a));this.ctr++},t.flush=function(){this.tags.forEach(function(a){var i;return(i=a.parentNode)==null?void 0:i.removeChild(a)}),this.tags=[],this.ctr=0},e})(),U="-ms-",Ie="-moz-",E="-webkit-",Tt="comm",tt="rule",nt="decl",na="@import",$t="@keyframes",ra="@layer",aa=Math.abs,Re=String.fromCharCode,sa=Object.assign;function ia(e,t){return Y(e,0)^45?(((t<<2^Y(e,0))<<2^Y(e,1))<<2^Y(e,2))<<2^Y(e,3):0}function Pt(e){return e.trim()}function oa(e,t){return(e=t.exec(e))?e[0]:e}function M(e,t,r){return e.replace(t,r)}function Ve(e,t){return e.indexOf(t)}function Y(e,t){return e.charCodeAt(t)|0}function me(e,t,r){return e.slice(t,r)}function K(e){return e.length}function rt(e){return e.length}function be(e,t){return t.push(e),e}function ca(e,t){return e.map(t).join("")}var Le=1,oe=1,Dt=0,W=0,D=0,ce="";function _e(e,t,r,a,i,s,o){return{value:e,root:t,parent:r,type:a,props:i,children:s,line:Le,column:oe,length:o,return:""}}function de(e,t){return sa(_e("",null,null,"",null,null,0),e,{length:-e.length},t)}function ua(){return D}function la(){return D=W>0?Y(ce,--W):0,oe--,D===10&&(oe=1,Le--),D}function G(){return D=W<Dt?Y(ce,W++):0,oe++,D===10&&(oe=1,Le++),D}function Q(){return Y(ce,W)}function Se(){return W}function ve(e,t){return me(ce,e,t)}function pe(e){switch(e){case 0:case 9:case 10:case 13:case 32:return 5;case 33:case 43:case 44:case 47:case 62:case 64:case 126:case 59:case 123:case 125:return 4;case 58:return 3;case 34:case 39:case 40:case 91:return 2;case 41:case 93:return 1}return 0}function zt(e){return Le=oe=1,Dt=K(ce=e),W=0,[]}function Bt(e){return ce="",e}function je(e){return Pt(ve(W-1,Ye(e===91?e+2:e===40?e+1:e)))}function fa(e){for(;(D=Q())&&D<33;)G();return pe(e)>2||pe(D)>3?"":" "}function da(e,t){for(;--t&&G()&&!(D<48||D>102||D>57&&D<65||D>70&&D<97););return ve(e,Se()+(t<6&&Q()==32&&G()==32))}function Ye(e){for(;G();)switch(D){case e:return W;case 34:case 39:e!==34&&e!==39&&Ye(D);break;case 40:e===41&&Ye(e);break;case 92:G();break}return W}function ma(e,t){for(;G()&&e+D!==57;)if(e+D===84&&Q()===47)break;return"/*"+ve(t,W-1)+"*"+Re(e===47?e:G())}function pa(e){for(;!pe(Q());)G();return ve(e,W)}function ha(e){return Bt(Ce("",null,null,null,[""],e=zt(e),0,[0],e))}function Ce(e,t,r,a,i,s,o,u,f){for(var p=0,h=0,y=o,S=0,x=0,b=0,g=1,N=1,I=1,j=0,C="",z=i,d=s,O=a,n=C;N;)switch(b=j,j=G()){case 40:if(b!=108&&Y(n,y-1)==58){Ve(n+=M(je(j),"&","&\f"),"&\f")!=-1&&(I=-1);break}case 34:case 39:case 91:n+=je(j);break;case 9:case 10:case 13:case 32:n+=fa(b);break;case 92:n+=da(Se()-1,7);continue;case 47:switch(Q()){case 42:case 47:be(ga(ma(G(),Se()),t,r),f);break;default:n+="/"}break;case 123*g:u[p++]=K(n)*I;case 125*g:case 59:case 0:switch(j){case 0:case 125:N=0;case 59+h:I==-1&&(n=M(n,/\f/g,"")),x>0&&K(n)-y&&be(x>32?mt(n+";",a,r,y-1):mt(M(n," ","")+";",a,r,y-2),f);break;case 59:n+=";";default:if(be(O=dt(n,t,r,p,h,i,u,C,z=[],d=[],y),s),j===123)if(h===0)Ce(n,t,O,O,z,s,y,u,d);else switch(S===99&&Y(n,3)===110?100:S){case 100:case 108:case 109:case 115:Ce(e,O,O,a&&be(dt(e,O,O,0,0,i,u,C,i,z=[],y),d),i,d,y,u,a?z:d);break;default:Ce(n,O,O,O,[""],d,0,u,d)}}p=h=x=0,g=I=1,C=n="",y=o;break;case 58:y=1+K(n),x=b;default:if(g<1){if(j==123)--g;else if(j==125&&g++==0&&la()==125)continue}switch(n+=Re(j),j*g){case 38:I=h>0?1:(n+="\f",-1);break;case 44:u[p++]=(K(n)-1)*I,I=1;break;case 64:Q()===45&&(n+=je(G())),S=Q(),h=y=K(C=n+=pa(Se())),j++;break;case 45:b===45&&K(n)==2&&(g=0)}}return s}function dt(e,t,r,a,i,s,o,u,f,p,h){for(var y=i-1,S=i===0?s:[""],x=rt(S),b=0,g=0,N=0;b<a;++b)for(var I=0,j=me(e,y+1,y=aa(g=o[b])),C=e;I<x;++I)(C=Pt(g>0?S[I]+" "+j:M(j,/&\f/g,S[I])))&&(f[N++]=C);return _e(e,t,r,i===0?tt:u,f,p,h)}function ga(e,t,r){return _e(e,t,r,Tt,Re(ua()),me(e,2,-2),0)}function mt(e,t,r,a){return _e(e,t,r,nt,me(e,0,a),me(e,a+1,-1),a)}function ae(e,t){for(var r="",a=rt(e),i=0;i<a;i++)r+=t(e[i],i,e,t)||"";return r}function ya(e,t,r,a){switch(e.type){case ra:if(e.children.length)break;case na:case nt:return e.return=e.return||e.value;case Tt:return"";case $t:return e.return=e.value+"{"+ae(e.children,a)+"}";case tt:e.value=e.props.join(",")}return K(r=ae(e.children,a))?e.return=e.value+"{"+r+"}":""}function va(e){var t=rt(e);return function(r,a,i,s){for(var o="",u=0;u<t;u++)o+=e[u](r,a,i,s)||"";return o}}function ba(e){return function(t){t.root||(t=t.return)&&e(t)}}function xa(e){var t=Object.create(null);return function(r){return t[r]===void 0&&(t[r]=e(r)),t[r]}}var ka=function(t,r,a){for(var i=0,s=0;i=s,s=Q(),i===38&&s===12&&(r[a]=1),!pe(s);)G();return ve(t,W)},wa=function(t,r){var a=-1,i=44;do switch(pe(i)){case 0:i===38&&Q()===12&&(r[a]=1),t[a]+=ka(W-1,r,a);break;case 2:t[a]+=je(i);break;case 4:if(i===44){t[++a]=Q()===58?"&\f":"",r[a]=t[a].length;break}default:t[a]+=Re(i)}while(i=G());return t},Sa=function(t,r){return Bt(wa(zt(t),r))},pt=new WeakMap,ja=function(t){if(!(t.type!=="rule"||!t.parent||t.length<1)){for(var r=t.value,a=t.parent,i=t.column===a.column&&t.line===a.line;a.type!=="rule";)if(a=a.parent,!a)return;if(!(t.props.length===1&&r.charCodeAt(0)!==58&&!pt.get(a))&&!i){pt.set(t,!0);for(var s=[],o=Sa(r,s),u=a.props,f=0,p=0;f<o.length;f++)for(var h=0;h<u.length;h++,p++)t.props[p]=s[f]?o[f].replace(/&\f/g,u[h]):u[h]+" "+o[f]}}},Ca=function(t){if(t.type==="decl"){var r=t.value;r.charCodeAt(0)===108&&r.charCodeAt(2)===98&&(t.return="",t.value="")}};function Ft(e,t){switch(ia(e,t)){case 5103:return E+"print-"+e+e;case 5737:case 4201:case 3177:case 3433:case 1641:case 4457:case 2921:case 5572:case 6356:case 5844:case 3191:case 6645:case 3005:case 6391:case 5879:case 5623:case 6135:case 4599:case 4855:case 4215:case 6389:case 5109:case 5365:case 5621:case 3829:return E+e+e;case 5349:case 4246:case 4810:case 6968:case 2756:return E+e+Ie+e+U+e+e;case 6828:case 4268:return E+e+U+e+e;case 6165:return E+e+U+"flex-"+e+e;case 5187:return E+e+M(e,/(\w+).+(:[^]+)/,E+"box-$1$2"+U+"flex-$1$2")+e;case 5443:return E+e+U+"flex-item-"+M(e,/flex-|-self/,"")+e;case 4675:return E+e+U+"flex-line-pack"+M(e,/align-content|flex-|-self/,"")+e;case 5548:return E+e+U+M(e,"shrink","negative")+e;case 5292:return E+e+U+M(e,"basis","preferred-size")+e;case 6060:return E+"box-"+M(e,"-grow","")+E+e+U+M(e,"grow","positive")+e;case 4554:return E+M(e,/([^-])(transform)/g,"$1"+E+"$2")+e;case 6187:return M(M(M(e,/(zoom-|grab)/,E+"$1"),/(image-set)/,E+"$1"),e,"")+e;case 5495:case 3959:return M(e,/(image-set\([^]*)/,E+"$1$`$1");case 4968:return M(M(e,/(.+:)(flex-)?(.*)/,E+"box-pack:$3"+U+"flex-pack:$3"),/s.+-b[^;]+/,"justify")+E+e+e;case 4095:case 3583:case 4068:case 2532:return M(e,/(.+)-inline(.+)/,E+"$1$2")+e;case 8116:case 7059:case 5753:case 5535:case 5445:case 5701:case 4933:case 4677:case 5533:case 5789:case 5021:case 4765:if(K(e)-1-t>6)switch(Y(e,t+1)){case 109:if(Y(e,t+4)!==45)break;case 102:return M(e,/(.+:)(.+)-([^]+)/,"$1"+E+"$2-$3$1"+Ie+(Y(e,t+3)==108?"$3":"$2-$3"))+e;case 115:return~Ve(e,"stretch")?Ft(M(e,"stretch","fill-available"),t)+e:e}break;case 4949:if(Y(e,t+1)!==115)break;case 6444:switch(Y(e,K(e)-3-(~Ve(e,"!important")&&10))){case 107:return M(e,":",":"+E)+e;case 101:return M(e,/(.+:)([^;!]+)(;|!.+)?/,"$1"+E+(Y(e,14)===45?"inline-":"")+"box$3$1"+E+"$2$3$1"+U+"$2box$3")+e}break;case 5936:switch(Y(e,t+11)){case 114:return E+e+U+M(e,/[svh]\w+-[tblr]{2}/,"tb")+e;case 108:return E+e+U+M(e,/[svh]\w+-[tblr]{2}/,"tb-rl")+e;case 45:return E+e+U+M(e,/[svh]\w+-[tblr]{2}/,"lr")+e}return E+e+U+e+e}return e}var Na=function(t,r,a,i){if(t.length>-1&&!t.return)switch(t.type){case nt:t.return=Ft(t.value,t.length);break;case $t:return ae([de(t,{value:M(t.value,"@","@"+E)})],i);case tt:if(t.length)return ca(t.props,function(s){switch(oa(s,/(::plac\w+|:read-\w+)/)){case":read-only":case":read-write":return ae([de(t,{props:[M(s,/:(read-\w+)/,":"+Ie+"$1")]})],i);case"::placeholder":return ae([de(t,{props:[M(s,/:(plac\w+)/,":"+E+"input-$1")]}),de(t,{props:[M(s,/:(plac\w+)/,":"+Ie+"$1")]}),de(t,{props:[M(s,/:(plac\w+)/,U+"input-$1")]})],i)}return""})}},Ia=[Na],Ea=function(t){var r=t.key;if(r==="css"){var a=document.querySelectorAll("style[data-emotion]:not([data-s])");Array.prototype.forEach.call(a,function(g){var N=g.getAttribute("data-emotion");N.indexOf(" ")!==-1&&(document.head.appendChild(g),g.setAttribute("data-s",""))})}var i=t.stylisPlugins||Ia,s={},o,u=[];o=t.container||document.head,Array.prototype.forEach.call(document.querySelectorAll('style[data-emotion^="'+r+' "]'),function(g){for(var N=g.getAttribute("data-emotion").split(" "),I=1;I<N.length;I++)s[N[I]]=!0;u.push(g)});var f,p=[ja,Ca];{var h,y=[ya,ba(function(g){h.insert(g)})],S=va(p.concat(i,y)),x=function(N){return ae(ha(N),S)};f=function(N,I,j,C){h=j,x(N?N+"{"+I.styles+"}":I.styles),C&&(b.inserted[I.name]=!0)}}var b={key:r,sheet:new ta({key:r,container:o,nonce:t.nonce,speedy:t.speedy,prepend:t.prepend,insertionPoint:t.insertionPoint}),nonce:t.nonce,inserted:s,registered:{},insert:f};return b.sheet.hydrate(u),b},Pe={exports:{}},A={};var ht;function Ma(){if(ht)return A;ht=1;var e=typeof Symbol=="function"&&Symbol.for,t=e?Symbol.for("react.element"):60103,r=e?Symbol.for("react.portal"):60106,a=e?Symbol.for("react.fragment"):60107,i=e?Symbol.for("react.strict_mode"):60108,s=e?Symbol.for("react.profiler"):60114,o=e?Symbol.for("react.provider"):60109,u=e?Symbol.for("react.context"):60110,f=e?Symbol.for("react.async_mode"):60111,p=e?Symbol.for("react.concurrent_mode"):60111,h=e?Symbol.for("react.forward_ref"):60112,y=e?Symbol.for("react.suspense"):60113,S=e?Symbol.for("react.suspense_list"):60120,x=e?Symbol.for("react.memo"):60115,b=e?Symbol.for("react.lazy"):60116,g=e?Symbol.for("react.block"):60121,N=e?Symbol.for("react.fundamental"):60117,I=e?Symbol.for("react.responder"):60118,j=e?Symbol.for("react.scope"):60119;function C(d){if(typeof d=="object"&&d!==null){var O=d.$$typeof;switch(O){case t:switch(d=d.type,d){case f:case p:case a:case s:case i:case y:return d;default:switch(d=d&&d.$$typeof,d){case u:case h:case b:case x:case o:return d;default:return O}}case r:return O}}}function z(d){return C(d)===p}return A.AsyncMode=f,A.ConcurrentMode=p,A.ContextConsumer=u,A.ContextProvider=o,A.Element=t,A.ForwardRef=h,A.Fragment=a,A.Lazy=b,A.Memo=x,A.Portal=r,A.Profiler=s,A.StrictMode=i,A.Suspense=y,A.isAsyncMode=function(d){return z(d)||C(d)===f},A.isConcurrentMode=z,A.isContextConsumer=function(d){return C(d)===u},A.isContextProvider=function(d){return C(d)===o},A.isElement=function(d){return typeof d=="object"&&d!==null&&d.$$typeof===t},A.isForwardRef=function(d){return C(d)===h},A.isFragment=function(d){return C(d)===a},A.isLazy=function(d){return C(d)===b},A.isMemo=function(d){return C(d)===x},A.isPortal=function(d){return C(d)===r},A.isProfiler=function(d){return C(d)===s},A.isStrictMode=function(d){return C(d)===i},A.isSuspense=function(d){return C(d)===y},A.isValidElementType=function(d){return typeof d=="string"||typeof d=="function"||d===a||d===p||d===s||d===i||d===y||d===S||typeof d=="object"&&d!==null&&(d.$$typeof===b||d.$$typeof===x||d.$$typeof===o||d.$$typeof===u||d.$$typeof===h||d.$$typeof===N||d.$$typeof===I||d.$$typeof===j||d.$$typeof===g)},A.typeOf=C,A}var gt;function Aa(){return gt||(gt=1,Pe.exports=Ma()),Pe.exports}var De,yt;function Ra(){if(yt)return De;yt=1;var e=Aa(),t={childContextTypes:!0,contextType:!0,contextTypes:!0,defaultProps:!0,displayName:!0,getDefaultProps:!0,getDerivedStateFromError:!0,getDerivedStateFromProps:!0,mixins:!0,propTypes:!0,type:!0},r={name:!0,length:!0,prototype:!0,caller:!0,callee:!0,arguments:!0,arity:!0},a={$$typeof:!0,render:!0,defaultProps:!0,displayName:!0,propTypes:!0},i={$$typeof:!0,compare:!0,defaultProps:!0,displayName:!0,propTypes:!0,type:!0},s={};s[e.ForwardRef]=a,s[e.Memo]=i;function o(b){return e.isMemo(b)?i:s[b.$$typeof]||t}var u=Object.defineProperty,f=Object.getOwnPropertyNames,p=Object.getOwnPropertySymbols,h=Object.getOwnPropertyDescriptor,y=Object.getPrototypeOf,S=Object.prototype;function x(b,g,N){if(typeof g!="string"){if(S){var I=y(g);I&&I!==S&&x(b,I,N)}var j=f(g);p&&(j=j.concat(p(g)));for(var C=o(b),z=o(g),d=0;d<j.length;++d){var O=j[d];if(!r[O]&&!(N&&N[O])&&!(z&&z[O])&&!(C&&C[O])){var n=h(g,O);try{u(b,O,n)}catch{}}}}return b}return De=x,De}Ra();var La=!0;function Vt(e,t,r){var a="";return r.split(" ").forEach(function(i){e[i]!==void 0?t.push(e[i]+";"):i&&(a+=i+" ")}),a}var at=function(t,r,a){var i=t.key+"-"+r.name;(a===!1||La===!1)&&t.registered[i]===void 0&&(t.registered[i]=r.styles)},Yt=function(t,r,a){at(t,r,a);var i=t.key+"-"+r.name;if(t.inserted[r.name]===void 0){var s=r;do t.insert(r===s?"."+i:"",s,t.sheet,!0),s=s.next;while(s!==void 0)}};function _a(e){for(var t=0,r,a=0,i=e.length;i>=4;++a,i-=4)r=e.charCodeAt(a)&255|(e.charCodeAt(++a)&255)<<8|(e.charCodeAt(++a)&255)<<16|(e.charCodeAt(++a)&255)<<24,r=(r&65535)*1540483477+((r>>>16)*59797<<16),r^=r>>>24,t=(r&65535)*1540483477+((r>>>16)*59797<<16)^(t&65535)*1540483477+((t>>>16)*59797<<16);switch(i){case 3:t^=(e.charCodeAt(a+2)&255)<<16;case 2:t^=(e.charCodeAt(a+1)&255)<<8;case 1:t^=e.charCodeAt(a)&255,t=(t&65535)*1540483477+((t>>>16)*59797<<16)}return t^=t>>>13,t=(t&65535)*1540483477+((t>>>16)*59797<<16),((t^t>>>15)>>>0).toString(36)}var Oa={animationIterationCount:1,aspectRatio:1,borderImageOutset:1,borderImageSlice:1,borderImageWidth:1,boxFlex:1,boxFlexGroup:1,boxOrdinalGroup:1,columnCount:1,columns:1,flex:1,flexGrow:1,flexPositive:1,flexShrink:1,flexNegative:1,flexOrder:1,gridRow:1,gridRowEnd:1,gridRowSpan:1,gridRowStart:1,gridColumn:1,gridColumnEnd:1,gridColumnSpan:1,gridColumnStart:1,msGridRow:1,msGridRowSpan:1,msGridColumn:1,msGridColumnSpan:1,fontWeight:1,lineHeight:1,opacity:1,order:1,orphans:1,scale:1,tabSize:1,widows:1,zIndex:1,zoom:1,WebkitLineClamp:1,fillOpacity:1,floodOpacity:1,stopOpacity:1,strokeDasharray:1,strokeDashoffset:1,strokeMiterlimit:1,strokeOpacity:1,strokeWidth:1},Ta=/[A-Z]|^ms/g,$a=/_EMO_([^_]+?)_([^]*?)_EMO_/g,Ut=function(t){return t.charCodeAt(1)===45},vt=function(t){return t!=null&&typeof t!="boolean"},ze=xa(function(e){return Ut(e)?e:e.replace(Ta,"-$&").toLowerCase()}),bt=function(t,r){switch(t){case"animation":case"animationName":if(typeof r=="string")return r.replace($a,function(a,i,s){return J={name:i,styles:s,next:J},i})}return Oa[t]!==1&&!Ut(t)&&typeof r=="number"&&r!==0?r+"px":r};function he(e,t,r){if(r==null)return"";var a=r;if(a.__emotion_styles!==void 0)return a;switch(typeof r){case"boolean":return"";case"object":{var i=r;if(i.anim===1)return J={name:i.name,styles:i.styles,next:J},i.name;var s=r;if(s.styles!==void 0){var o=s.next;if(o!==void 0)for(;o!==void 0;)J={name:o.name,styles:o.styles,next:J},o=o.next;var u=s.styles+";";return u}return Pa(e,t,r)}case"function":{if(e!==void 0){var f=J,p=r(e);return J=f,he(e,t,p)}break}}var h=r;if(t==null)return h;var y=t[h];return y!==void 0?y:h}function Pa(e,t,r){var a="";if(Array.isArray(r))for(var i=0;i<r.length;i++)a+=he(e,t,r[i])+";";else for(var s in r){var o=r[s];if(typeof o!="object"){var u=o;t!=null&&t[u]!==void 0?a+=s+"{"+t[u]+"}":vt(u)&&(a+=ze(s)+":"+bt(s,u)+";")}else if(Array.isArray(o)&&typeof o[0]=="string"&&(t==null||t[o[0]]===void 0))for(var f=0;f<o.length;f++)vt(o[f])&&(a+=ze(s)+":"+bt(s,o[f])+";");else{var p=he(e,t,o);switch(s){case"animation":case"animationName":{a+=ze(s)+":"+p+";";break}default:a+=s+"{"+p+"}"}}}return a}var xt=/label:\s*([^\s;{]+)\s*(;|$)/g,J;function st(e,t,r){if(e.length===1&&typeof e[0]=="object"&&e[0]!==null&&e[0].styles!==void 0)return e[0];var a=!0,i="";J=void 0;var s=e[0];if(s==null||s.raw===void 0)a=!1,i+=he(r,t,s);else{var o=s;i+=o[0]}for(var u=1;u<e.length;u++)if(i+=he(r,t,e[u]),a){var f=s;i+=f[u]}xt.lastIndex=0;for(var p="",h;(h=xt.exec(i))!==null;)p+="-"+h[1];var y=_a(i)+p;return{name:y,styles:i,next:J}}var Da=function(t){return t()},za=lt.useInsertionEffect?lt.useInsertionEffect:!1,Xt=za||Da,Wt=v.createContext(typeof HTMLElement<"u"?Ea({key:"css"}):null);Wt.Provider;var Gt=function(t){return v.forwardRef(function(r,a){var i=v.useContext(Wt);return t(r,i,a)})},Ht=v.createContext({}),Oe={}.hasOwnProperty,Ue="__EMOTION_TYPE_PLEASE_DO_NOT_USE__",qt=function(t,r){var a={};for(var i in r)Oe.call(r,i)&&(a[i]=r[i]);return a[Ue]=t,a},Ba=function(t){var r=t.cache,a=t.serialized,i=t.isStringTag;return at(r,a,i),Xt(function(){return Yt(r,a,i)}),null},Fa=Gt(function(e,t,r){var a=e.css;typeof a=="string"&&t.registered[a]!==void 0&&(a=t.registered[a]);var i=e[Ue],s=[a],o="";typeof e.className=="string"?o=Vt(t.registered,s,e.className):e.className!=null&&(o=e.className+" ");var u=st(s,void 0,v.useContext(Ht));o+=t.key+"-"+u.name;var f={};for(var p in e)Oe.call(e,p)&&p!=="css"&&p!==Ue&&(f[p]=e[p]);return f.className=o,r&&(f.ref=r),v.createElement(v.Fragment,null,v.createElement(Ba,{cache:t,serialized:u,isStringTag:typeof i=="string"}),v.createElement(i,f))}),Kt=Fa,Va=c.Fragment,F=function(t,r,a){return Oe.call(r,"css")?c.jsx(Kt,qt(t,r),a):c.jsx(t,r,a)},kt=function(t,r){var a=arguments;if(r==null||!Oe.call(r,"css"))return v.createElement.apply(void 0,a);var i=a.length,s=new Array(i);s[0]=Kt,s[1]=qt(t,r);for(var o=2;o<i;o++)s[o]=a[o];return v.createElement.apply(null,s)};(function(e){var t;t||(t=e.JSX||(e.JSX={}))})(kt||(kt={}));function Jt(){for(var e=arguments.length,t=new Array(e),r=0;r<e;r++)t[r]=arguments[r];return st(t)}function l(){var e=Jt.apply(void 0,arguments),t="animation-"+e.name;return{name:t,styles:"@keyframes "+t+"{"+e.styles+"}",anim:1,toString:function(){return"_EMO_"+this.name+"_"+this.styles+"_EMO_"}}}var Ya=function e(t){for(var r=t.length,a=0,i="";a<r;a++){var s=t[a];if(s!=null){var o=void 0;switch(typeof s){case"boolean":break;case"object":{if(Array.isArray(s))o=e(s);else{o="";for(var u in s)s[u]&&u&&(o&&(o+=" "),o+=u)}break}default:o=s}o&&(i&&(i+=" "),i+=o)}}return i};function Ua(e,t,r){var a=[],i=Vt(e,a,r);return a.length<2?r:i+t(a)}var Xa=function(t){var r=t.cache,a=t.serializedArr;return Xt(function(){for(var i=0;i<a.length;i++)Yt(r,a[i],!1)}),null},Be=Gt(function(e,t){var r=[],a=function(){for(var f=arguments.length,p=new Array(f),h=0;h<f;h++)p[h]=arguments[h];var y=st(p,t.registered);return r.push(y),at(t,y,!1),t.key+"-"+y.name},i=function(){for(var f=arguments.length,p=new Array(f),h=0;h<f;h++)p[h]=arguments[h];return Ua(t.registered,a,Ya(p))},s={css:a,cx:i,theme:v.useContext(Ht)},o=e.children(s);return v.createElement(v.Fragment,null,v.createElement(Xa,{cache:t,serializedArr:r}),o)}),Wa=Object.defineProperty,Ga=(e,t,r)=>t in e?Wa(e,t,{enumerable:!0,configurable:!0,writable:!0,value:r}):e[t]=r,xe=(e,t,r)=>Ga(e,typeof t!="symbol"?t+"":t,r),Xe=new Map,ke=new WeakMap,wt=0,Ha=void 0;function qa(e){return e?(ke.has(e)||(wt+=1,ke.set(e,wt.toString())),ke.get(e)):"0"}function Ka(e){return Object.keys(e).sort().filter(t=>e[t]!==void 0).map(t=>`${t}_${t==="root"?qa(e.root):e[t]}`).toString()}function Ja(e){const t=Ka(e);let r=Xe.get(t);if(!r){const a=new Map;let i;const s=new IntersectionObserver(o=>{o.forEach(u=>{var f;const p=u.isIntersecting&&i.some(h=>u.intersectionRatio>=h);e.trackVisibility&&typeof u.isVisible>"u"&&(u.isVisible=p),(f=a.get(u.target))==null||f.forEach(h=>{h(p,u)})})},e);i=s.thresholds||(Array.isArray(e.threshold)?e.threshold:[e.threshold||0]),r={id:t,observer:s,elements:a},Xe.set(t,r)}return r}function Qt(e,t,r={},a=Ha){if(typeof window.IntersectionObserver>"u"&&a!==void 0){const f=e.getBoundingClientRect();return t(a,{isIntersecting:a,target:e,intersectionRatio:typeof r.threshold=="number"?r.threshold:0,time:0,boundingClientRect:f,intersectionRect:f,rootBounds:f}),()=>{}}const{id:i,observer:s,elements:o}=Ja(r),u=o.get(e)||[];return o.has(e)||o.set(e,u),u.push(t),s.observe(e),function(){u.splice(u.indexOf(t),1),u.length===0&&(o.delete(e),s.unobserve(e)),o.size===0&&(s.disconnect(),Xe.delete(i))}}function Qa(e){return typeof e.children!="function"}var St=class extends v.Component{constructor(e){super(e),xe(this,"node",null),xe(this,"_unobserveCb",null),xe(this,"handleNode",t=>{this.node&&(this.unobserve(),!t&&!this.props.triggerOnce&&!this.props.skip&&this.setState({inView:!!this.props.initialInView,entry:void 0})),this.node=t||null,this.observeNode()}),xe(this,"handleChange",(t,r)=>{t&&this.props.triggerOnce&&this.unobserve(),Qa(this.props)||this.setState({inView:t,entry:r}),this.props.onChange&&this.props.onChange(t,r)}),this.state={inView:!!e.initialInView,entry:void 0}}componentDidMount(){this.unobserve(),this.observeNode()}componentDidUpdate(e){(e.rootMargin!==this.props.rootMargin||e.root!==this.props.root||e.threshold!==this.props.threshold||e.skip!==this.props.skip||e.trackVisibility!==this.props.trackVisibility||e.delay!==this.props.delay)&&(this.unobserve(),this.observeNode())}componentWillUnmount(){this.unobserve()}observeNode(){if(!this.node||this.props.skip)return;const{threshold:e,root:t,rootMargin:r,trackVisibility:a,delay:i,fallbackInView:s}=this.props;this._unobserveCb=Qt(this.node,this.handleChange,{threshold:e,root:t,rootMargin:r,trackVisibility:a,delay:i},s)}unobserve(){this._unobserveCb&&(this._unobserveCb(),this._unobserveCb=null)}render(){const{children:e}=this.props;if(typeof e=="function"){const{inView:x,entry:b}=this.state;return e({inView:x,entry:b,ref:this.handleNode})}const{as:t,triggerOnce:r,threshold:a,root:i,rootMargin:s,onChange:o,skip:u,trackVisibility:f,delay:p,initialInView:h,fallbackInView:y,...S}=this.props;return v.createElement(t||"div",{ref:this.handleNode,...S},e)}};function Zt({threshold:e,delay:t,trackVisibility:r,rootMargin:a,root:i,triggerOnce:s,skip:o,initialInView:u,fallbackInView:f,onChange:p}={}){var h;const[y,S]=v.useState(null),x=v.useRef(p),[b,g]=v.useState({inView:!!u,entry:void 0});x.current=p,v.useEffect(()=>{if(o||!y)return;let C;return C=Qt(y,(z,d)=>{g({inView:z,entry:d}),x.current&&x.current(z,d),d.isIntersecting&&s&&C&&(C(),C=void 0)},{root:i,rootMargin:a,threshold:e,trackVisibility:r,delay:t},f),()=>{C&&C()}},[Array.isArray(e)?e.toString():e,y,i,a,s,o,r,f,t]);const N=(h=b.entry)==null?void 0:h.target,I=v.useRef(void 0);!y&&N&&!s&&!o&&I.current!==N&&(I.current=N,g({inView:!!u,entry:void 0}));const j=[S,b.inView,b.entry];return j.ref=j[0],j.inView=j[1],j.entry=j[2],j}l`
  from,
  20%,
  53%,
  to {
    animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1);
    transform: translate3d(0, 0, 0);
  }

  40%,
  43% {
    animation-timing-function: cubic-bezier(0.755, 0.05, 0.855, 0.06);
    transform: translate3d(0, -30px, 0) scaleY(1.1);
  }

  70% {
    animation-timing-function: cubic-bezier(0.755, 0.05, 0.855, 0.06);
    transform: translate3d(0, -15px, 0) scaleY(1.05);
  }

  80% {
    transition-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1);
    transform: translate3d(0, 0, 0) scaleY(0.95);
  }

  90% {
    transform: translate3d(0, -4px, 0) scaleY(1.02);
  }
`;l`
  from,
  50%,
  to {
    opacity: 1;
  }

  25%,
  75% {
    opacity: 0;
  }
`;l`
  0% {
    transform: translateX(0);
  }

  6.5% {
    transform: translateX(-6px) rotateY(-9deg);
  }

  18.5% {
    transform: translateX(5px) rotateY(7deg);
  }

  31.5% {
    transform: translateX(-3px) rotateY(-5deg);
  }

  43.5% {
    transform: translateX(2px) rotateY(3deg);
  }

  50% {
    transform: translateX(0);
  }
`;l`
  0% {
    transform: scale(1);
  }

  14% {
    transform: scale(1.3);
  }

  28% {
    transform: scale(1);
  }

  42% {
    transform: scale(1.3);
  }

  70% {
    transform: scale(1);
  }
`;l`
  from,
  11.1%,
  to {
    transform: translate3d(0, 0, 0);
  }

  22.2% {
    transform: skewX(-12.5deg) skewY(-12.5deg);
  }

  33.3% {
    transform: skewX(6.25deg) skewY(6.25deg);
  }

  44.4% {
    transform: skewX(-3.125deg) skewY(-3.125deg);
  }

  55.5% {
    transform: skewX(1.5625deg) skewY(1.5625deg);
  }

  66.6% {
    transform: skewX(-0.78125deg) skewY(-0.78125deg);
  }

  77.7% {
    transform: skewX(0.390625deg) skewY(0.390625deg);
  }

  88.8% {
    transform: skewX(-0.1953125deg) skewY(-0.1953125deg);
  }
`;l`
  from {
    transform: scale3d(1, 1, 1);
  }

  50% {
    transform: scale3d(1.05, 1.05, 1.05);
  }

  to {
    transform: scale3d(1, 1, 1);
  }
`;l`
  from {
    transform: scale3d(1, 1, 1);
  }

  30% {
    transform: scale3d(1.25, 0.75, 1);
  }

  40% {
    transform: scale3d(0.75, 1.25, 1);
  }

  50% {
    transform: scale3d(1.15, 0.85, 1);
  }

  65% {
    transform: scale3d(0.95, 1.05, 1);
  }

  75% {
    transform: scale3d(1.05, 0.95, 1);
  }

  to {
    transform: scale3d(1, 1, 1);
  }
`;l`
  from,
  to {
    transform: translate3d(0, 0, 0);
  }

  10%,
  30%,
  50%,
  70%,
  90% {
    transform: translate3d(-10px, 0, 0);
  }

  20%,
  40%,
  60%,
  80% {
    transform: translate3d(10px, 0, 0);
  }
`;l`
  from,
  to {
    transform: translate3d(0, 0, 0);
  }

  10%,
  30%,
  50%,
  70%,
  90% {
    transform: translate3d(-10px, 0, 0);
  }

  20%,
  40%,
  60%,
  80% {
    transform: translate3d(10px, 0, 0);
  }
`;l`
  from,
  to {
    transform: translate3d(0, 0, 0);
  }

  10%,
  30%,
  50%,
  70%,
  90% {
    transform: translate3d(0, -10px, 0);
  }

  20%,
  40%,
  60%,
  80% {
    transform: translate3d(0, 10px, 0);
  }
`;l`
  20% {
    transform: rotate3d(0, 0, 1, 15deg);
  }

  40% {
    transform: rotate3d(0, 0, 1, -10deg);
  }

  60% {
    transform: rotate3d(0, 0, 1, 5deg);
  }

  80% {
    transform: rotate3d(0, 0, 1, -5deg);
  }

  to {
    transform: rotate3d(0, 0, 1, 0deg);
  }
`;l`
  from {
    transform: scale3d(1, 1, 1);
  }

  10%,
  20% {
    transform: scale3d(0.9, 0.9, 0.9) rotate3d(0, 0, 1, -3deg);
  }

  30%,
  50%,
  70%,
  90% {
    transform: scale3d(1.1, 1.1, 1.1) rotate3d(0, 0, 1, 3deg);
  }

  40%,
  60%,
  80% {
    transform: scale3d(1.1, 1.1, 1.1) rotate3d(0, 0, 1, -3deg);
  }

  to {
    transform: scale3d(1, 1, 1);
  }
`;l`
  from {
    transform: translate3d(0, 0, 0);
  }

  15% {
    transform: translate3d(-25%, 0, 0) rotate3d(0, 0, 1, -5deg);
  }

  30% {
    transform: translate3d(20%, 0, 0) rotate3d(0, 0, 1, 3deg);
  }

  45% {
    transform: translate3d(-15%, 0, 0) rotate3d(0, 0, 1, -3deg);
  }

  60% {
    transform: translate3d(10%, 0, 0) rotate3d(0, 0, 1, 2deg);
  }

  75% {
    transform: translate3d(-5%, 0, 0) rotate3d(0, 0, 1, -1deg);
  }

  to {
    transform: translate3d(0, 0, 0);
  }
`;const Za=l`
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
`,es=l`
  from {
    opacity: 0;
    transform: translate3d(-100%, 100%, 0);
  }

  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
`,ts=l`
  from {
    opacity: 0;
    transform: translate3d(100%, 100%, 0);
  }

  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
`,ns=l`
  from {
    opacity: 0;
    transform: translate3d(0, -100%, 0);
  }

  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
`,rs=l`
  from {
    opacity: 0;
    transform: translate3d(0, -2000px, 0);
  }

  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
`,it=l`
  from {
    opacity: 0;
    transform: translate3d(-100%, 0, 0);
  }

  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
`,as=l`
  from {
    opacity: 0;
    transform: translate3d(-2000px, 0, 0);
  }

  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
`,ss=l`
  from {
    opacity: 0;
    transform: translate3d(100%, 0, 0);
  }

  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
`,is=l`
  from {
    opacity: 0;
    transform: translate3d(2000px, 0, 0);
  }

  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
`,os=l`
  from {
    opacity: 0;
    transform: translate3d(-100%, -100%, 0);
  }

  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
`,cs=l`
  from {
    opacity: 0;
    transform: translate3d(100%, -100%, 0);
  }

  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
`,us=l`
  from {
    opacity: 0;
    transform: translate3d(0, 100%, 0);
  }

  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
`,ls=l`
  from {
    opacity: 0;
    transform: translate3d(0, 2000px, 0);
  }

  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
`;function fs({duration:e=1e3,delay:t=0,timingFunction:r="ease",keyframes:a=it,iterationCount:i=1}){return Jt`
    animation-duration: ${e}ms;
    animation-timing-function: ${r};
    animation-delay: ${t}ms;
    animation-name: ${a};
    animation-direction: normal;
    animation-fill-mode: both;
    animation-iteration-count: ${i};

    @media (prefers-reduced-motion: reduce) {
      animation: none;
    }
  `}function ds(e){return e==null}function ms(e){return typeof e=="string"||typeof e=="number"||typeof e=="boolean"}function en(e,t){return r=>r?e():t()}function ge(e){return en(e,()=>null)}function We(e){return ge(()=>({opacity:0}))(e)}const tn=e=>{const{cascade:t=!1,damping:r=.5,delay:a=0,duration:i=1e3,fraction:s=0,keyframes:o=it,triggerOnce:u=!1,className:f,style:p,childClassName:h,childStyle:y,children:S,onVisibilityChange:x}=e,b=v.useMemo(()=>fs({keyframes:o,duration:i}),[i,o]);return ds(S)?null:ms(S)?F(hs,{...e,animationStyles:b,children:String(S)}):jr.isFragment(S)?F(nn,{...e,animationStyles:b}):F(Va,{children:v.Children.map(S,(g,N)=>{if(!v.isValidElement(g))return null;const I=a+(t?N*i*r:0);switch(g.type){case"ol":case"ul":return F(Be,{children:({cx:j})=>F(g.type,{...g.props,className:j(f,g.props.className),style:Object.assign({},p,g.props.style),children:F(tn,{...e,children:g.props.children})})});case"li":return F(St,{threshold:s,triggerOnce:u,onChange:x,children:({inView:j,ref:C})=>F(Be,{children:({cx:z})=>F(g.type,{...g.props,ref:C,className:z(h,g.props.className),css:ge(()=>b)(j),style:Object.assign({},y,g.props.style,We(!j),{animationDelay:I+"ms"})})})});default:return F(St,{threshold:s,triggerOnce:u,onChange:x,children:({inView:j,ref:C})=>F("div",{ref:C,className:f,css:ge(()=>b)(j),style:Object.assign({},p,We(!j),{animationDelay:I+"ms"}),children:F(Be,{children:({cx:z})=>F(g.type,{...g.props,className:z(h,g.props.className),style:Object.assign({},y,g.props.style)})})})})}})})},ps={display:"inline-block",whiteSpace:"pre"},hs=e=>{const{animationStyles:t,cascade:r=!1,damping:a=.5,delay:i=0,duration:s=1e3,fraction:o=0,triggerOnce:u=!1,className:f,style:p,children:h,onVisibilityChange:y}=e,{ref:S,inView:x}=Zt({triggerOnce:u,threshold:o,onChange:y});return en(()=>F("div",{ref:S,className:f,style:Object.assign({},p,ps),children:h.split("").map((b,g)=>F("span",{css:ge(()=>t)(x),style:{animationDelay:i+g*s*a+"ms"},children:b},g))}),()=>F(nn,{...e,children:h}))(r)},nn=e=>{const{animationStyles:t,fraction:r=0,triggerOnce:a=!1,className:i,style:s,children:o,onVisibilityChange:u}=e,{ref:f,inView:p}=Zt({triggerOnce:a,threshold:r,onChange:u});return F("div",{ref:f,className:i,css:ge(()=>t)(p),style:Object.assign({},s,We(!p)),children:o})};l`
  from,
  20%,
  40%,
  60%,
  80%,
  to {
    animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1);
  }

  0% {
    opacity: 0;
    transform: scale3d(0.3, 0.3, 0.3);
  }

  20% {
    transform: scale3d(1.1, 1.1, 1.1);
  }

  40% {
    transform: scale3d(0.9, 0.9, 0.9);
  }

  60% {
    opacity: 1;
    transform: scale3d(1.03, 1.03, 1.03);
  }

  80% {
    transform: scale3d(0.97, 0.97, 0.97);
  }

  to {
    opacity: 1;
    transform: scale3d(1, 1, 1);
  }
`;l`
  from,
  60%,
  75%,
  90%,
  to {
    animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1);
  }

  0% {
    opacity: 0;
    transform: translate3d(0, -3000px, 0) scaleY(3);
  }

  60% {
    opacity: 1;
    transform: translate3d(0, 25px, 0) scaleY(0.9);
  }

  75% {
    transform: translate3d(0, -10px, 0) scaleY(0.95);
  }

  90% {
    transform: translate3d(0, 5px, 0) scaleY(0.985);
  }

  to {
    transform: translate3d(0, 0, 0);
  }
`;l`
  from,
  60%,
  75%,
  90%,
  to {
    animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1);
  }

  0% {
    opacity: 0;
    transform: translate3d(-3000px, 0, 0) scaleX(3);
  }

  60% {
    opacity: 1;
    transform: translate3d(25px, 0, 0) scaleX(1);
  }

  75% {
    transform: translate3d(-10px, 0, 0) scaleX(0.98);
  }

  90% {
    transform: translate3d(5px, 0, 0) scaleX(0.995);
  }

  to {
    transform: translate3d(0, 0, 0);
  }
`;l`
  from,
  60%,
  75%,
  90%,
  to {
    animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1);
  }

  from {
    opacity: 0;
    transform: translate3d(3000px, 0, 0) scaleX(3);
  }

  60% {
    opacity: 1;
    transform: translate3d(-25px, 0, 0) scaleX(1);
  }

  75% {
    transform: translate3d(10px, 0, 0) scaleX(0.98);
  }

  90% {
    transform: translate3d(-5px, 0, 0) scaleX(0.995);
  }

  to {
    transform: translate3d(0, 0, 0);
  }
`;l`
  from,
  60%,
  75%,
  90%,
  to {
    animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1);
  }

  from {
    opacity: 0;
    transform: translate3d(0, 3000px, 0) scaleY(5);
  }

  60% {
    opacity: 1;
    transform: translate3d(0, -20px, 0) scaleY(0.9);
  }

  75% {
    transform: translate3d(0, 10px, 0) scaleY(0.95);
  }

  90% {
    transform: translate3d(0, -5px, 0) scaleY(0.985);
  }

  to {
    transform: translate3d(0, 0, 0);
  }
`;l`
  20% {
    transform: scale3d(0.9, 0.9, 0.9);
  }

  50%,
  55% {
    opacity: 1;
    transform: scale3d(1.1, 1.1, 1.1);
  }

  to {
    opacity: 0;
    transform: scale3d(0.3, 0.3, 0.3);
  }
`;l`
  20% {
    transform: translate3d(0, 10px, 0) scaleY(0.985);
  }

  40%,
  45% {
    opacity: 1;
    transform: translate3d(0, -20px, 0) scaleY(0.9);
  }

  to {
    opacity: 0;
    transform: translate3d(0, 2000px, 0) scaleY(3);
  }
`;l`
  20% {
    opacity: 1;
    transform: translate3d(20px, 0, 0) scaleX(0.9);
  }

  to {
    opacity: 0;
    transform: translate3d(-2000px, 0, 0) scaleX(2);
  }
`;l`
  20% {
    opacity: 1;
    transform: translate3d(-20px, 0, 0) scaleX(0.9);
  }

  to {
    opacity: 0;
    transform: translate3d(2000px, 0, 0) scaleX(2);
  }
`;l`
  20% {
    transform: translate3d(0, -10px, 0) scaleY(0.985);
  }

  40%,
  45% {
    opacity: 1;
    transform: translate3d(0, 20px, 0) scaleY(0.9);
  }

  to {
    opacity: 0;
    transform: translate3d(0, -2000px, 0) scaleY(3);
  }
`;const gs=l`
  from {
    opacity: 1;
  }

  to {
    opacity: 0;
  }
`,ys=l`
  from {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }

  to {
    opacity: 0;
    transform: translate3d(-100%, 100%, 0);
  }
`,vs=l`
  from {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }

  to {
    opacity: 0;
    transform: translate3d(100%, 100%, 0);
  }
`,bs=l`
  from {
    opacity: 1;
  }

  to {
    opacity: 0;
    transform: translate3d(0, 100%, 0);
  }
`,xs=l`
  from {
    opacity: 1;
  }

  to {
    opacity: 0;
    transform: translate3d(0, 2000px, 0);
  }
`,ks=l`
  from {
    opacity: 1;
  }

  to {
    opacity: 0;
    transform: translate3d(-100%, 0, 0);
  }
`,ws=l`
  from {
    opacity: 1;
  }

  to {
    opacity: 0;
    transform: translate3d(-2000px, 0, 0);
  }
`,Ss=l`
  from {
    opacity: 1;
  }

  to {
    opacity: 0;
    transform: translate3d(100%, 0, 0);
  }
`,js=l`
  from {
    opacity: 1;
  }

  to {
    opacity: 0;
    transform: translate3d(2000px, 0, 0);
  }
`,Cs=l`
  from {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }

  to {
    opacity: 0;
    transform: translate3d(-100%, -100%, 0);
  }
`,Ns=l`
  from {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }

  to {
    opacity: 0;
    transform: translate3d(100%, -100%, 0);
  }
`,Is=l`
  from {
    opacity: 1;
  }

  to {
    opacity: 0;
    transform: translate3d(0, -100%, 0);
  }
`,Es=l`
  from {
    opacity: 1;
  }

  to {
    opacity: 0;
    transform: translate3d(0, -2000px, 0);
  }
`;function Ms(e,t,r){switch(r){case"bottom-left":return t?ys:es;case"bottom-right":return t?vs:ts;case"down":return e?t?xs:rs:t?bs:ns;case"left":return e?t?ws:as:t?ks:it;case"right":return e?t?js:is:t?Ss:ss;case"top-left":return t?Cs:os;case"top-right":return t?Ns:cs;case"up":return e?t?Es:ls:t?Is:us;default:return t?gs:Za}}const As=e=>{const{big:t=!1,direction:r,reverse:a=!1,...i}=e,s=v.useMemo(()=>Ms(t,a,r),[t,r,a]);return F(tn,{keyframes:s,...i})};l`
  from {
    transform: perspective(400px) scale3d(1, 1, 1) translate3d(0, 0, 0) rotate3d(0, 1, 0, -360deg);
    animation-timing-function: ease-out;
  }

  40% {
    transform: perspective(400px) scale3d(1, 1, 1) translate3d(0, 0, 150px)
      rotate3d(0, 1, 0, -190deg);
    animation-timing-function: ease-out;
  }

  50% {
    transform: perspective(400px) scale3d(1, 1, 1) translate3d(0, 0, 150px)
      rotate3d(0, 1, 0, -170deg);
    animation-timing-function: ease-in;
  }

  80% {
    transform: perspective(400px) scale3d(0.95, 0.95, 0.95) translate3d(0, 0, 0)
      rotate3d(0, 1, 0, 0deg);
    animation-timing-function: ease-in;
  }

  to {
    transform: perspective(400px) scale3d(1, 1, 1) translate3d(0, 0, 0) rotate3d(0, 1, 0, 0deg);
    animation-timing-function: ease-in;
  }
`;l`
  from {
    transform: perspective(400px) rotate3d(1, 0, 0, 90deg);
    animation-timing-function: ease-in;
    opacity: 0;
  }

  40% {
    transform: perspective(400px) rotate3d(1, 0, 0, -20deg);
    animation-timing-function: ease-in;
  }

  60% {
    transform: perspective(400px) rotate3d(1, 0, 0, 10deg);
    opacity: 1;
  }

  80% {
    transform: perspective(400px) rotate3d(1, 0, 0, -5deg);
  }

  to {
    transform: perspective(400px);
  }
`;l`
  from {
    transform: perspective(400px) rotate3d(0, 1, 0, 90deg);
    animation-timing-function: ease-in;
    opacity: 0;
  }

  40% {
    transform: perspective(400px) rotate3d(0, 1, 0, -20deg);
    animation-timing-function: ease-in;
  }

  60% {
    transform: perspective(400px) rotate3d(0, 1, 0, 10deg);
    opacity: 1;
  }

  80% {
    transform: perspective(400px) rotate3d(0, 1, 0, -5deg);
  }

  to {
    transform: perspective(400px);
  }
`;l`
  from {
    transform: perspective(400px);
  }

  30% {
    transform: perspective(400px) rotate3d(1, 0, 0, -20deg);
    opacity: 1;
  }

  to {
    transform: perspective(400px) rotate3d(1, 0, 0, 90deg);
    opacity: 0;
  }
`;l`
  from {
    transform: perspective(400px);
  }

  30% {
    transform: perspective(400px) rotate3d(0, 1, 0, -15deg);
    opacity: 1;
  }

  to {
    transform: perspective(400px) rotate3d(0, 1, 0, 90deg);
    opacity: 0;
  }
`;l`
  0% {
    animation-timing-function: ease-in-out;
  }

  20%,
  60% {
    transform: rotate3d(0, 0, 1, 80deg);
    animation-timing-function: ease-in-out;
  }

  40%,
  80% {
    transform: rotate3d(0, 0, 1, 60deg);
    animation-timing-function: ease-in-out;
    opacity: 1;
  }

  to {
    transform: translate3d(0, 700px, 0);
    opacity: 0;
  }
`;l`
  from {
    opacity: 0;
    transform: scale(0.1) rotate(30deg);
    transform-origin: center bottom;
  }

  50% {
    transform: rotate(-10deg);
  }

  70% {
    transform: rotate(3deg);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
`;l`
  from {
    opacity: 0;
    transform: translate3d(-100%, 0, 0) rotate3d(0, 0, 1, -120deg);
  }

  to {
    opacity: 1;
    transform: translate3d(0, 0, 0);
  }
`;l`
  from {
    opacity: 1;
  }

  to {
    opacity: 0;
    transform: translate3d(100%, 0, 0) rotate3d(0, 0, 1, 120deg);
  }
`;l`
  from {
    transform: rotate3d(0, 0, 1, -200deg);
    opacity: 0;
  }

  to {
    transform: translate3d(0, 0, 0);
    opacity: 1;
  }
`;l`
  from {
    transform: rotate3d(0, 0, 1, -45deg);
    opacity: 0;
  }

  to {
    transform: translate3d(0, 0, 0);
    opacity: 1;
  }
`;l`
  from {
    transform: rotate3d(0, 0, 1, 45deg);
    opacity: 0;
  }

  to {
    transform: translate3d(0, 0, 0);
    opacity: 1;
  }
`;l`
  from {
    transform: rotate3d(0, 0, 1, 45deg);
    opacity: 0;
  }

  to {
    transform: translate3d(0, 0, 0);
    opacity: 1;
  }
`;l`
  from {
    transform: rotate3d(0, 0, 1, -90deg);
    opacity: 0;
  }

  to {
    transform: translate3d(0, 0, 0);
    opacity: 1;
  }
`;l`
  from {
    opacity: 1;
  }

  to {
    transform: rotate3d(0, 0, 1, 200deg);
    opacity: 0;
  }
`;l`
  from {
    opacity: 1;
  }

  to {
    transform: rotate3d(0, 0, 1, 45deg);
    opacity: 0;
  }
`;l`
  from {
    opacity: 1;
  }

  to {
    transform: rotate3d(0, 0, 1, -45deg);
    opacity: 0;
  }
`;l`
  from {
    opacity: 1;
  }

  to {
    transform: rotate3d(0, 0, 1, -45deg);
    opacity: 0;
  }
`;l`
  from {
    opacity: 1;
  }

  to {
    transform: rotate3d(0, 0, 1, 90deg);
    opacity: 0;
  }
`;l`
  from {
    transform: translate3d(0, -100%, 0);
    visibility: visible;
  }

  to {
    transform: translate3d(0, 0, 0);
  }
`;l`
  from {
    transform: translate3d(-100%, 0, 0);
    visibility: visible;
  }

  to {
    transform: translate3d(0, 0, 0);
  }
`;l`
  from {
    transform: translate3d(100%, 0, 0);
    visibility: visible;
  }

  to {
    transform: translate3d(0, 0, 0);
  }
`;l`
  from {
    transform: translate3d(0, 100%, 0);
    visibility: visible;
  }

  to {
    transform: translate3d(0, 0, 0);
  }
`;l`
  from {
    transform: translate3d(0, 0, 0);
  }

  to {
    visibility: hidden;
    transform: translate3d(0, 100%, 0);
  }
`;l`
  from {
    transform: translate3d(0, 0, 0);
  }

  to {
    visibility: hidden;
    transform: translate3d(-100%, 0, 0);
  }
`;l`
  from {
    transform: translate3d(0, 0, 0);
  }

  to {
    visibility: hidden;
    transform: translate3d(100%, 0, 0);
  }
`;l`
  from {
    transform: translate3d(0, 0, 0);
  }

  to {
    visibility: hidden;
    transform: translate3d(0, -100%, 0);
  }
`;l`
  from {
    opacity: 0;
    transform: scale3d(0.3, 0.3, 0.3);
  }

  50% {
    opacity: 1;
  }
`;l`
  from {
    opacity: 0;
    transform: scale3d(0.1, 0.1, 0.1) translate3d(0, -1000px, 0);
    animation-timing-function: cubic-bezier(0.55, 0.055, 0.675, 0.19);
  }

  60% {
    opacity: 1;
    transform: scale3d(0.475, 0.475, 0.475) translate3d(0, 60px, 0);
    animation-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1);
  }
`;l`
  from {
    opacity: 0;
    transform: scale3d(0.1, 0.1, 0.1) translate3d(-1000px, 0, 0);
    animation-timing-function: cubic-bezier(0.55, 0.055, 0.675, 0.19);
  }

  60% {
    opacity: 1;
    transform: scale3d(0.475, 0.475, 0.475) translate3d(10px, 0, 0);
    animation-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1);
  }
`;l`
  from {
    opacity: 0;
    transform: scale3d(0.1, 0.1, 0.1) translate3d(1000px, 0, 0);
    animation-timing-function: cubic-bezier(0.55, 0.055, 0.675, 0.19);
  }

  60% {
    opacity: 1;
    transform: scale3d(0.475, 0.475, 0.475) translate3d(-10px, 0, 0);
    animation-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1);
  }
`;l`
  from {
    opacity: 0;
    transform: scale3d(0.1, 0.1, 0.1) translate3d(0, 1000px, 0);
    animation-timing-function: cubic-bezier(0.55, 0.055, 0.675, 0.19);
  }

  60% {
    opacity: 1;
    transform: scale3d(0.475, 0.475, 0.475) translate3d(0, -60px, 0);
    animation-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1);
  }
`;l`
  from {
    opacity: 1;
  }

  50% {
    opacity: 0;
    transform: scale3d(0.3, 0.3, 0.3);
  }

  to {
    opacity: 0;
  }
`;l`
  40% {
    opacity: 1;
    transform: scale3d(0.475, 0.475, 0.475) translate3d(0, -60px, 0);
    animation-timing-function: cubic-bezier(0.55, 0.055, 0.675, 0.19);
  }

  to {
    opacity: 0;
    transform: scale3d(0.1, 0.1, 0.1) translate3d(0, 2000px, 0);
    animation-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1);
  }
`;l`
  40% {
    opacity: 1;
    transform: scale3d(0.475, 0.475, 0.475) translate3d(42px, 0, 0);
  }

  to {
    opacity: 0;
    transform: scale(0.1) translate3d(-2000px, 0, 0);
  }
`;l`
  40% {
    opacity: 1;
    transform: scale3d(0.475, 0.475, 0.475) translate3d(-42px, 0, 0);
  }

  to {
    opacity: 0;
    transform: scale(0.1) translate3d(2000px, 0, 0);
  }
`;l`
  40% {
    opacity: 1;
    transform: scale3d(0.475, 0.475, 0.475) translate3d(0, 60px, 0);
    animation-timing-function: cubic-bezier(0.55, 0.055, 0.675, 0.19);
  }

  to {
    opacity: 0;
    transform: scale3d(0.1, 0.1, 0.1) translate3d(0, -2000px, 0);
    animation-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1);
  }
`;const Rs="/resources/images/cxVEzTBI.webp",Ls="/resources/images/oWee6f7C.webp",_s="bPuI4IpU",Os="dK4HjHa1",Ts="_6TVY6KVX",$s="ZEtzXAqe",Ps="xrCjPqxq",Ds="KGAfFxu3",zs="A7vaaFML",Bs="_2WMigrmw",Fs="dQLKG9DB",Vs="lb-jt3Gz",Ys="h8jEsQWn",Us="sD1UdUn0",Xs="T5rnlpGr",Ws="ntQP2EKR",Gs="_4uP-LXi2",V={instructions:_s,content:Os,sideImage:Ts,summaryLine:$s,summaryIcon:Ps,text:Ds,title:zs,subtitle:Bs,divider:Fs,buildings:Vs,image:Ys,lastTitle:Us,expensiveCountry:Xs,countryImage:Ws,sadIcon:Gs};function Hs({animateIn:e=!1}){const t=rn(e);return c.jsxs("div",{className:V.instructions,children:[c.jsxs("div",{className:V.content,children:[c.jsx("h1",{children:"How to play"}),c.jsx(we,{icon:jn,iconColor:"#81be97",title:"All players start with $1500.",animateIn:e}),c.jsx(we,{icon:Cn,iconColor:"#ffa1a1",title:"On your turn, roll the dice to move forward.",subtitle:"Got doubles? You’ll have another turn!",animateIn:e}),c.jsx(we,{icon:Nn,iconColor:"#ffdba1",title:"Purchase valuable properties and grow your financial empire.",subtitle:"Once you own a property, other players will pay rent when they land on it.",animateIn:e}),c.jsx(jt,{}),c.jsxs(Ge,{className:V.buildings,triggerOnce:!0,duration:t,children:[c.jsxs("div",{className:V.text,children:[c.jsxs("div",{className:V.title,children:["Own a full property set?",c.jsx("br",{}),"Start building houses and hotels"]}),c.jsxs("div",{className:V.subtitle,children:["Players will pay you a large amount of money when they land on properties with buildings.",c.jsx("br",{}),"Build hotels to maximize income and make other players lose their money."]})]}),c.jsx("div",{className:V.image,children:c.jsx(qs,{})})]}),c.jsx(jt,{}),c.jsx(we,{icon:In,title:c.jsx("span",{className:V.lastTitle,children:"Be rich. Get richer. Do not bankrupt."}),iconColor:"#d49cff",animateIn:e})]}),c.jsx(Ge,{className:V.sideImage,triggerOnce:!0,duration:t,children:c.jsx("img",{src:Ls,alt:"owned property"})})]})}function we({icon:e,iconColor:t="",title:r,subtitle:a,animateIn:i=!1}){const s=rn(i);return c.jsxs(Ge,{className:V.summaryLine,triggerOnce:!0,duration:s,children:[c.jsx("div",{className:V.summaryIcon,style:{color:t},children:c.jsx(X,{icon:e,fixedWidth:!0})}),c.jsxs("div",{className:V.text,children:[c.jsx("div",{className:V.title,children:r}),c.jsx("div",{className:V.subtitle,children:a})]})]})}function jt(){return c.jsx("div",{className:V.divider})}function qs(){return c.jsxs("div",{className:V.expensiveCountry,children:[c.jsx("img",{className:V.countryImage,src:Rs,alt:"country-with-buildings"}),c.jsx("img",{className:V.sadIcon,src:Ir,alt:"sad-because-expensive"})]})}function rn(e){return e?500:0}function Ge({children:e,className:t,duration:r,...a}){return c.jsx(As,{...a,delay:r&&100,duration:r,children:c.jsx("div",{className:t,children:e})})}function Ks(e,t){const[r,a]=v.useState(e);e!==r&&(a(e),t(r,e))}function Js(e){const[t,r]=v.useState(!e),a=Ae(),i=v.useRef([]);return Ks(e,()=>r(!e)),v.useEffect(()=>{const s=i.current;e&&En(e),gr(e).then(o=>{if(e&&!o.roomData){Mn("room_not_found"),An(e),a({to:"/",replace:!0});return}e&&Rn(),s.push(...o.playingRooms.map(u=>Ln(u))),r(!0)})},[e,a]),Lt(()=>{i.current.forEach(s=>ie.dismiss(s))}),t}const Qs="F0q-YRc4",Zs="sROjnmMA",ei="_6PzUdqon",ti="q9MIh4iG",ni="SJmyf9uz",ri="_2KDKhIb2",ai="Xx-WiRQ1",si="joVkhBop",ii="wgKNjHrC",oi="J4AU8Ewq",ci="_9zpci2yF",H={maintenanceMessage:Qs,icon:Zs,tool:ei,boom:ti,title:ni,description:ri,progressContainer:ai,progress:si,discordMsg:ii,discordIcon:oi,dismiss:ci};function ui({dismiss:e}){const{maintenanceInfo:t}=v.useContext(Me);return c.jsxs("div",{className:H.maintenanceMessage,children:[c.jsx(fi,{onClick:e}),c.jsxs("div",{className:H.icon,children:[c.jsx(X,{icon:_n,className:H.tool}),c.jsx(X,{icon:Ke,className:H.boom})]}),c.jsx("div",{className:H.title,children:"Richup is getting an update"}),c.jsxs("div",{className:H.description,children:["The servers are currently under maintenance.",c.jsx("br",{}),"Come back in a few minutes."]}),c.jsx(yr,{progressBarClassName:H.progress,containerClassName:H.progressContainer,progress:t.progress}),c.jsx(li,{})]})}function li({className:e}){return c.jsxs(Je,{className:[H.discordMsg,e],children:["For more updates, join",c.jsxs("a",{href:Tn,target:"_blank",rel:"noreferrer noopener",onClick:On,children:[c.jsx(X,{icon:$n,className:H.discordIcon}),"Richup on Discord"]})]})}function fi({onClick:e}){return c.jsx("div",{className:H.dismiss,onClick:e,children:c.jsx(X,{icon:pr})})}const di=60;function an({publishedAt:e,expiresAt:t},r){return Date.parse(e)<=r&&r<Date.parse(t)}function Te(e){return e.startsWith("/")&&!/^\/[/\\]/.test(e)}async function mi(){const{data:e}=await Qe.get("/announcements");return e}function sn(){return _t({queryKey:["announcements"],queryFn:mi,staleTime:di*1e3})}function pi(e){Ze("announcement_shown",{announcement_id:e})}function hi(e){Ze("announcement_reopened",{announcement_id:e})}function gi(e,t){Ze("announcement_click",{announcement_id:e,announcement_type:t?"internal":"external"})}const yi="hex5vGbD",vi="_1SS6B1ut",bi="_8f09V1j3",xi="_4rL4cNyM",ki="_4jlpo3Qv",wi="wisA85Z9",Si="KA8tmYmB",ji="c73IE474",Ci="ht4w8pPv",Ni="Shu3OmC7",q={announcement:yi,close:vi,eyebrow:bi,sparkles:xi,contents:ki,art:wi,wideImage:Si,title:ji,body:Ci,readMore:Ni};function Ii({announcement:e,onLinkClick:t}){const{title:r,body:a,link:i,image:s}=e,o=s!=null&&!Ei(s);return c.jsxs("div",{className:o?void 0:q.contents,children:[s&&(o?c.jsx(Pn,{src:s,className:q.wideImage}):c.jsx(Er,{image:s,className:q.art})),c.jsxs("div",{children:[c.jsxs("div",{className:q.eyebrow,children:[c.jsx(X,{icon:Ke,className:q.sparkles}),"New"]}),c.jsx("div",{className:q.title,children:r}),c.jsx("div",{className:q.body,children:a}),i&&c.jsx(se,{small:!0,noMargin:!0,className:q.readMore,iconEnd:c.jsx(X,{icon:Dn}),onClick:t&&(()=>t(i)),children:Te(i)?"Check it out":"Read more"})]})]})}function Ei(e){return e.startsWith("__")}function Mi(e,t){const{id:r}=e;return ie(()=>c.jsx(Ii,{announcement:e,onLinkClick:a=>{gi(r,Te(a)),t(a)}}),{className:q.announcement,position:"bottom-center",autoClose:!1,toastId:Ee(r),icon:!1,closeButton:a=>c.jsx(zn,{...a,className:q.close})})}function Ee(e){return`announcement:${e}`}const Ai=2147483647;function on(e,t){const{id:r,expiresAt:a}=e;Mi(e,t);const i=Date.parse(a)-Date.now(),s=i<=Ai?window.setTimeout(()=>ie.dismiss(Ee(r)),i):void 0;return()=>{window.clearTimeout(s),ie.dismiss(Ee(r))}}const cn="seen-announcements";function ye(){return qe(cn,[])}function un(e,t){const r=[...new Set([...ye(),e])];Bn(cn,Ri(r,t))}function Ne(e,t){return e?.filter(({id:r})=>!t.includes(r)).reduce((r,a)=>!r||Date.parse(a.publishedAt)>Date.parse(r.publishedAt)?a:r,void 0)}function Ri(e,t){const r=new Set(t);return e.filter(a=>r.has(a))}function Li(){const{data:e}=sn(),t=Ot(),[r]=v.useState(ye),[a]=v.useState(Date.now),[i,s]=v.useState(),o=Ne(e?.filter(u=>an(u,a)),r);return o&&e&&!i&&s({announcement:o,liveIds:e.map(({id:u})=>u)}),v.useEffect(()=>{if(!i)return;const{announcement:u,liveIds:f}=i;if(!(Date.parse(u.expiresAt)-Date.now()<=0||ye().includes(u.id)))return un(u.id,f),pi(u.id),on(u,y=>{Te(y)?t.history.push(y):window.open(y,"_blank","noopener,noreferrer")})},[i,t]),null}const _i="_68oFZATJ",Oi="QaToMBkX",Ct={icon:_i,dot:Oi},Ti=3e4;function $i({className:e}){const{data:t}=sn(),r=Ot(),[a,i]=v.useState(ye),s=v.useRef(void 0);v.useEffect(()=>()=>s.current?.(),[]);const o=Cr(t?.length?Ti:null),u=Nt(t,o),f=Ne(u,[]),p=Ne(u,a)!=null;if(Pi(f&&Ee(f.id))||!f)return null;function y(){const S=Nt(t,Vn()),x=Ne(S,[]);if(!x||!S){window.open(Fn,"_blank","noopener,noreferrer");return}un(x.id,S.map(({id:b})=>b)),i(ye()),hi(x.id),s.current?.(),s.current=on(x,b=>{Te(b)?r.history.push(b):window.open(b,"_blank","noopener,noreferrer")})}return c.jsxs(se,{className:e,type:"subtle",small:!0,noMargin:!0,onClick:y,icon:c.jsx(X,{icon:Ke,className:Ct.icon}),children:["What's new",p&&c.jsx("span",{className:Ct.dot})]})}function Nt(e,t){return e?.filter(r=>an(r,t))}function Pi(e){const t=v.useCallback(r=>ie.onChange(r),[]);return v.useSyncExternalStore(t,()=>e!=null&&ie.isActive(e),()=>!1)}const Di="gPV8ilB3",zi={container:Di};function Bi({until:e}){return c.jsxs("div",{className:zi.container,children:[c.jsx("h3",{children:"You are banned from Richup.io"}),c.jsxs("p",{children:["It means you have violated our"," ",c.jsx(Yn,{to:"/terms-and-conditions",children:"Terms and conditions"}),"."]}),c.jsxs("small",{children:["Your ban will be lifted on"," ",c.jsx("i",{children:ft.fromJSDate(e).toLocaleString(ft.DATETIME_FULL)})]})]})}function Fi({isLoadingAds:e=!1,delayMs:t}){const r=Un();return Xn(()=>{let a=!1;const i=()=>{r.getState().start(e),a=!0};let s=null;return t!==void 0?s=setTimeout(()=>{i(),a=!0},t):i(),()=>{a&&r.getState().stop(),s!==null&&clearTimeout(s)}},[e,r]),null}var Fe={exports:{}},It;function Vi(){return It||(It=1,(function(e){(function(){var t=Object.assign||function(n){for(var m,w=1;w<arguments.length;w++){m=arguments[w];for(var k in m)N(m,k)&&(n[k]=m[k])}return n},r=Array.isArray||function(n){return Object.prototype.toString.call(n)==="[object Array]"},a=u(["χρόνος","χρόνια"],["μήνας","μήνες"],["εβδομάδα","εβδομάδες"],["μέρα","μέρες"],["ώρα","ώρες"],["λεπτό","λεπτά"],["δευτερόλεπτο","δευτερόλεπτα"],["χιλιοστό του δευτερολέπτου","χιλιοστά του δευτερολέπτου"],","),i={af:u(["jaar","jaar"],["maand","maande"],["week","weke"],["dag","dae"],["uur","ure"],["minuut","minute"],["sekonde","sekondes"],["millisekonde","millisekondes"],","),am:s("ዓመት","ወር","ሳምንት","ቀን","ሰዓት","ደቂቃ","ሰከንድ","ሚሊሰከንድ"),ar:t(s(function(n){return["سنة","سنتان","سنوات"][y(n)]},function(n){return["شهر","شهران","أشهر"][y(n)]},function(n){return["أسبوع","أسبوعين","أسابيع"][y(n)]},function(n){return["يوم","يومين","أيام"][y(n)]},function(n){return["ساعة","ساعتين","ساعات"][y(n)]},function(n){return["دقيقة","دقيقتان","دقائق"][y(n)]},function(n){return["ثانية","ثانيتان","ثواني"][y(n)]},function(n){return["جزء من الثانية","جزآن من الثانية","أجزاء من الثانية"][y(n)]},","),{delimiter:" ﻭ ",_hideCountIf2:!0,_digitReplacements:["۰","١","٢","٣","٤","٥","٦","٧","٨","٩"]}),bg:h(["години","година","години"],["месеца","месец","месеца"],["седмици","седмица","седмици"],["дни","ден","дни"],["часа","час","часа"],["минути","минута","минути"],["секунди","секунда","секунди"],["милисекунди","милисекунда","милисекунди"]),bn:s("বছর","মাস","সপ্তাহ","দিন","ঘন্টা","মিনিট","সেকেন্ড","মিলিসেকেন্ড"),ca:u(["any","anys"],["mes","mesos"],["setmana","setmanes"],["dia","dies"],["hora","hores"],["minut","minuts"],["segon","segons"],["milisegon","milisegons"],","),ckb:s("ساڵ","مانگ","هەفتە","ڕۆژ","کاژێر","خولەک","چرکە","میلی چرکە","."),cs:s(function(n){return["rok","roku","roky","let"][x(n)]},function(n){return["měsíc","měsíce","měsíce","měsíců"][x(n)]},function(n){return["týden","týdne","týdny","týdnů"][x(n)]},function(n){return["den","dne","dny","dní"][x(n)]},function(n){return["hodina","hodiny","hodiny","hodin"][x(n)]},function(n){return["minuta","minuty","minuty","minut"][x(n)]},function(n){return["sekunda","sekundy","sekundy","sekund"][x(n)]},function(n){return["milisekunda","milisekundy","milisekundy","milisekund"][x(n)]},","),cy:s("flwyddyn","mis","wythnos","diwrnod","awr","munud","eiliad","milieiliad"),da:u(["år","år"],["måned","måneder"],["uge","uger"],["dag","dage"],["time","timer"],["minut","minutter"],["sekund","sekunder"],["millisekund","millisekunder"],","),de:u(["Jahr","Jahre"],["Monat","Monate"],["Woche","Wochen"],["Tag","Tage"],["Stunde","Stunden"],["Minute","Minuten"],["Sekunde","Sekunden"],["Millisekunde","Millisekunden"],","),el:a,en:u(["year","years"],["month","months"],["week","weeks"],["day","days"],["hour","hours"],["minute","minutes"],["second","seconds"],["millisecond","milliseconds"]),eo:u(["jaro","jaroj"],["monato","monatoj"],["semajno","semajnoj"],["tago","tagoj"],["horo","horoj"],["minuto","minutoj"],["sekundo","sekundoj"],["milisekundo","milisekundoj"],","),es:u(["año","años"],["mes","meses"],["semana","semanas"],["día","días"],["hora","horas"],["minuto","minutos"],["segundo","segundos"],["milisegundo","milisegundos"],","),et:u(["aasta","aastat"],["kuu","kuud"],["nädal","nädalat"],["päev","päeva"],["tund","tundi"],["minut","minutit"],["sekund","sekundit"],["millisekund","millisekundit"],","),eu:s("urte","hilabete","aste","egun","ordu","minutu","segundo","milisegundo",","),fa:s("سال","ماه","هفته","روز","ساعت","دقیقه","ثانیه","میلی ثانیه"),fi:u(["vuosi","vuotta"],["kuukausi","kuukautta"],["viikko","viikkoa"],["päivä","päivää"],["tunti","tuntia"],["minuutti","minuuttia"],["sekunti","sekuntia"],["millisekunti","millisekuntia"],","),fo:u(["ár","ár"],["mánaður","mánaðir"],["vika","vikur"],["dagur","dagar"],["tími","tímar"],["minuttur","minuttir"],["sekund","sekund"],["millisekund","millisekund"],","),fr:s(function(n){return"an"+(n>=2?"s":"")},"mois",function(n){return"semaine"+(n>=2?"s":"")},function(n){return"jour"+(n>=2?"s":"")},function(n){return"heure"+(n>=2?"s":"")},function(n){return"minute"+(n>=2?"s":"")},function(n){return"seconde"+(n>=2?"s":"")},function(n){return"milliseconde"+(n>=2?"s":"")},","),gr:a,he:u(["שנה","שנים"],["חודש","חודשים"],["שבוע","שבועות"],["יום","ימים"],["שעה","שעות"],["דקה","דקות"],["שניה","שניות"],["מילישנייה","מילישניות"]),hr:s(function(n){return n%10===2||n%10===3||n%10===4?"godine":"godina"},function(n){return n===1?"mjesec":n===2||n===3||n===4?"mjeseca":"mjeseci"},function(n){return n%10===1&&n!==11?"tjedan":"tjedna"},o(["dan","dana"]),function(n){return n===1?"sat":n===2||n===3||n===4?"sata":"sati"},function(n){var m=n%10;return(m===2||m===3||m===4)&&(n<10||n>14)?"minute":"minuta"},function(n){var m=n%10;return m===5||Math.floor(n)===n&&n>=10&&n<=19?"sekundi":m===1?"sekunda":m===2||m===3||m===4?"sekunde":"sekundi"},function(n){return n===1?"milisekunda":n%10===2||n%10===3||n%10===4?"milisekunde":"milisekundi"},","),hi:s("साल",o(["महीना","महीने"]),o(["हफ़्ता","हफ्ते"]),"दिन",o(["घंटा","घंटे"]),"मिनट","सेकंड","मिलीसेकंड"),hu:s("év","hónap","hét","nap","óra","perc","másodperc","ezredmásodperc",","),id:s("tahun","bulan","minggu","hari","jam","menit","detik","milidetik"),is:u(["ár","ár"],["mánuður","mánuðir"],["vika","vikur"],["dagur","dagar"],["klukkutími","klukkutímar"],["mínúta","mínútur"],["sekúnda","sekúndur"],["millisekúnda","millisekúndur"]),it:u(["anno","anni"],["mese","mesi"],["settimana","settimane"],["giorno","giorni"],["ora","ore"],["minuto","minuti"],["secondo","secondi"],["millisecondo","millisecondi"],","),ja:s("年","ヶ月","週間","日","時間","分","秒","ミリ秒"),km:s("ឆ្នាំ","ខែ","សប្តាហ៍","ថ្ងៃ","ម៉ោង","នាទី","វិនាទី","មិល្លីវិនាទី"),kn:u(["ವರ್ಷ","ವರ್ಷಗಳು"],["ತಿಂಗಳು","ತಿಂಗಳುಗಳು"],["ವಾರ","ವಾರಗಳು"],["ದಿನ","ದಿನಗಳು"],["ಗಂಟೆ","ಗಂಟೆಗಳು"],["ನಿಮಿಷ","ನಿಮಿಷಗಳು"],["ಸೆಕೆಂಡ್","ಸೆಕೆಂಡುಗಳು"],["ಮಿಲಿಸೆಕೆಂಡ್","ಮಿಲಿಸೆಕೆಂಡುಗಳು"]),ko:s("년","개월","주일","일","시간","분","초","밀리 초"),ku:s("sal","meh","hefte","roj","seet","deqe","saniye","mîlîçirk",","),lo:s("ປີ","ເດືອນ","ອາທິດ","ມື້","ຊົ່ວໂມງ","ນາທີ","ວິນາທີ","ມິນລິວິນາທີ",","),lt:s(function(n){return n%10===0||n%100>=10&&n%100<=20?"metų":"metai"},function(n){return["mėnuo","mėnesiai","mėnesių"][b(n)]},function(n){return["savaitė","savaitės","savaičių"][b(n)]},function(n){return["diena","dienos","dienų"][b(n)]},function(n){return["valanda","valandos","valandų"][b(n)]},function(n){return["minutė","minutės","minučių"][b(n)]},function(n){return["sekundė","sekundės","sekundžių"][b(n)]},function(n){return["milisekundė","milisekundės","milisekundžių"][b(n)]},","),lv:s(function(n){return g(n)?"gads":"gadi"},function(n){return g(n)?"mēnesis":"mēneši"},function(n){return g(n)?"nedēļa":"nedēļas"},function(n){return g(n)?"diena":"dienas"},function(n){return g(n)?"stunda":"stundas"},function(n){return g(n)?"minūte":"minūtes"},function(n){return g(n)?"sekunde":"sekundes"},function(n){return g(n)?"milisekunde":"milisekundes"},","),mk:u(["година","години"],["месец","месеци"],["недела","недели"],["ден","дена"],["час","часа"],["минута","минути"],["секунда","секунди"],["милисекунда","милисекунди"],","),mn:s("жил","сар","долоо хоног","өдөр","цаг","минут","секунд","миллисекунд"),mr:s(o(["वर्ष","वर्षे"]),o(["महिना","महिने"]),o(["आठवडा","आठवडे"]),"दिवस","तास",o(["मिनिट","मिनिटे"]),"सेकंद","मिलिसेकंद"),ms:s("tahun","bulan","minggu","hari","jam","minit","saat","milisaat"),nl:u(["jaar","jaar"],["maand","maanden"],["week","weken"],["dag","dagen"],["uur","uur"],["minuut","minuten"],["seconde","seconden"],["milliseconde","milliseconden"],","),no:u(["år","år"],["måned","måneder"],["uke","uker"],["dag","dager"],["time","timer"],["minutt","minutter"],["sekund","sekunder"],["millisekund","millisekunder"],","),pl:s(function(n){return["rok","roku","lata","lat"][S(n)]},function(n){return["miesiąc","miesiąca","miesiące","miesięcy"][S(n)]},function(n){return["tydzień","tygodnia","tygodnie","tygodni"][S(n)]},function(n){return["dzień","dnia","dni","dni"][S(n)]},function(n){return["godzina","godziny","godziny","godzin"][S(n)]},function(n){return["minuta","minuty","minuty","minut"][S(n)]},function(n){return["sekunda","sekundy","sekundy","sekund"][S(n)]},function(n){return["milisekunda","milisekundy","milisekundy","milisekund"][S(n)]},","),pt:u(["ano","anos"],["mês","meses"],["semana","semanas"],["dia","dias"],["hora","horas"],["minuto","minutos"],["segundo","segundos"],["milissegundo","milissegundos"],","),ro:s(f("an","ani","de ani"),f("lună","luni","de luni"),f("săptămână","săptămâni","de săptămâni"),f("zi","zile","de zile"),f("oră","ore","de ore"),f("minut","minute","de minute"),f("secundă","secunde","de secunde"),f("milisecundă","milisecunde","de milisecunde"),","),ru:h(["лет","год","года"],["месяцев","месяц","месяца"],["недель","неделя","недели"],["дней","день","дня"],["часов","час","часа"],["минут","минута","минуты"],["секунд","секунда","секунды"],["миллисекунд","миллисекунда","миллисекунды"]),sq:s(o(["vit","vjet"]),"muaj","javë","ditë","orë",function(n){return"minut"+(n===1?"ë":"a")},function(n){return"sekond"+(n===1?"ë":"a")},function(n){return"milisekond"+(n===1?"ë":"a")},","),sr:h(["години","година","године"],["месеци","месец","месеца"],["недељи","недеља","недеље"],["дани","дан","дана"],["сати","сат","сата"],["минута","минут","минута"],["секунди","секунда","секунде"],["милисекунди","милисекунда","милисекунде"]),sr_Latn:h(["godini","godina","godine"],["meseci","mesec","meseca"],["nedelji","nedelja","nedelje"],["dani","dan","dana"],["sati","sat","sata"],["minuta","minut","minuta"],["sekundi","sekunda","sekunde"],["milisekundi","milisekunda","milisekunde"]),ta:u(["வருடம்","ஆண்டுகள்"],["மாதம்","மாதங்கள்"],["வாரம்","வாரங்கள்"],["நாள்","நாட்கள்"],["மணி","மணிநேரம்"],["நிமிடம்","நிமிடங்கள்"],["வினாடி","வினாடிகள்"],["மில்லி விநாடி","மில்லி விநாடிகள்"]),te:u(["సంవత్సరం","సంవత్సరాల"],["నెల","నెలల"],["వారం","వారాలు"],["రోజు","రోజులు"],["గంట","గంటలు"],["నిమిషం","నిమిషాలు"],["సెకను","సెకన్లు"],["మిల్లీసెకన్","మిల్లీసెకన్లు"]),uk:h(["років","рік","роки"],["місяців","місяць","місяці"],["тижнів","тиждень","тижні"],["днів","день","дні"],["годин","година","години"],["хвилин","хвилина","хвилини"],["секунд","секунда","секунди"],["мілісекунд","мілісекунда","мілісекунди"]),ur:s("سال",o(["مہینہ","مہینے"]),o(["ہفتہ","ہفتے"]),"دن",o(["گھنٹہ","گھنٹے"]),"منٹ","سیکنڈ","ملی سیکنڈ"),sk:s(function(n){return["rok","roky","roky","rokov"][x(n)]},function(n){return["mesiac","mesiace","mesiace","mesiacov"][x(n)]},function(n){return["týždeň","týždne","týždne","týždňov"][x(n)]},function(n){return["deň","dni","dni","dní"][x(n)]},function(n){return["hodina","hodiny","hodiny","hodín"][x(n)]},function(n){return["minúta","minúty","minúty","minút"][x(n)]},function(n){return["sekunda","sekundy","sekundy","sekúnd"][x(n)]},function(n){return["milisekunda","milisekundy","milisekundy","milisekúnd"][x(n)]},","),sl:s(function(n){return n%10===1?"leto":n%100===2?"leti":n%100===3||n%100===4||Math.floor(n)!==n&&n%100<=5?"leta":"let"},function(n){return n%10===1?"mesec":n%100===2||Math.floor(n)!==n&&n%100<=5?"meseca":n%10===3||n%10===4?"mesece":"mesecev"},function(n){return n%10===1?"teden":n%10===2||Math.floor(n)!==n&&n%100<=4?"tedna":n%10===3||n%10===4?"tedne":"tednov"},function(n){return n%100===1?"dan":"dni"},function(n){return n%10===1?"ura":n%100===2?"uri":n%10===3||n%10===4||Math.floor(n)!==n?"ure":"ur"},function(n){return n%10===1?"minuta":n%10===2?"minuti":n%10===3||n%10===4||Math.floor(n)!==n&&n%100<=4?"minute":"minut"},function(n){return n%10===1?"sekunda":n%100===2?"sekundi":n%100===3||n%100===4||Math.floor(n)!==n?"sekunde":"sekund"},function(n){return n%10===1?"milisekunda":n%100===2?"milisekundi":n%100===3||n%100===4||Math.floor(n)!==n?"milisekunde":"milisekund"},","),sv:u(["år","år"],["månad","månader"],["vecka","veckor"],["dag","dagar"],["timme","timmar"],["minut","minuter"],["sekund","sekunder"],["millisekund","millisekunder"],","),sw:t(u(["mwaka","miaka"],["mwezi","miezi"],["wiki","wiki"],["siku","masiku"],["saa","masaa"],["dakika","dakika"],["sekunde","sekunde"],["milisekunde","milisekunde"]),{_numberFirst:!0}),tr:s("yıl","ay","hafta","gün","saat","dakika","saniye","milisaniye",","),th:s("ปี","เดือน","สัปดาห์","วัน","ชั่วโมง","นาที","วินาที","มิลลิวินาที"),uz:s("yil","oy","hafta","kun","soat","minut","sekund","millisekund"),uz_CYR:s("йил","ой","ҳафта","кун","соат","минут","секунд","миллисекунд"),vi:s("năm","tháng","tuần","ngày","giờ","phút","giây","mili giây",","),zh_CN:s("年","个月","周","天","小时","分钟","秒","毫秒"),zh_TW:s("年","個月","周","天","小時","分鐘","秒","毫秒")};function s(n,m,w,k,R,P,L,T,B){var _={y:n,mo:m,w,d:k,h:R,m:P,s:L,ms:T};return B&&(_.decimal=B),_}function o(n){return function(m){return m===1?n[0]:n[1]}}function u(n,m,w,k,R,P,L,T,B){return s(o(n),o(m),o(w),o(k),o(R),o(P),o(L),o(T),B)}function f(n,m,w){return function(k){if(k===1)return n;if(Math.floor(k)!==k||k===0)return m;var R=k%100;return R>=1&&R<=19?m:w}}function p(n){return function(m){return Math.floor(m)!==m?n[2]:m%100>=5&&m%100<=20||m%10>=5&&m%10<=9||m%10===0?n[0]:m%10===1?n[1]:m>1?n[2]:n[1]}}function h(n,m,w,k,R,P,L,T){return s(p(n),p(m),p(w),p(k),p(R),p(P),p(L),p(T),",")}function y(n){return n===2?1:n>2&&n<11?2:0}function S(n){return n===1?0:Math.floor(n)!==n?1:n%10>=2&&n%10<=4&&!(n%100>10&&n%100<20)?2:3}function x(n){return n===1?0:Math.floor(n)!==n?1:n%10>=2&&n%10<=4&&n%100<10?2:3}function b(n){return n===1||n%10===1&&n%100>20?0:Math.floor(n)!==n||n%10>=2&&n%100>20||n%10>=2&&n%100<10?1:2}function g(n){return n%10===1&&n%100!==11}function N(n,m){return Object.prototype.hasOwnProperty.call(n,m)}function I(n){var m=[n.language];if(N(n,"fallbacks"))if(r(n.fallbacks)&&n.fallbacks.length)m=m.concat(n.fallbacks);else throw new Error("fallbacks must be an array with at least one element");for(var w=0;w<m.length;w++){var k=m[w];if(N(n.languages,k))return n.languages[k];if(N(i,k))return i[k]}throw new Error("No language found.")}function j(n,m,w){var k=n.unitName,R=n.unitCount,P=w.spacer,L=w.maxDecimalPoints,T;N(w,"decimal")?T=w.decimal:N(m,"decimal")?T=m.decimal:T=".";var B;"digitReplacements"in w?B=w.digitReplacements:"_digitReplacements"in m&&(B=m._digitReplacements);var _,ue=L===void 0?R:Math.floor(R*Math.pow(10,L))/Math.pow(10,L),le=ue.toString();if(m._hideCountIf2&&R===2)_="",P="";else if(B){_="";for(var ee=0;ee<le.length;ee++){var te=le[ee];te==="."?_+=T:_+=B[te]}}else _=le.replace(".",T);var Z=m[k],ne;return typeof Z=="function"?ne=Z(R):ne=Z,m._numberFirst?ne+P+_:_+P+ne}function C(n,m){var w,k,R,P,L=m.units,T=m.unitMeasures,B="largest"in m?m.largest:1/0;if(!L.length)return[];var _={};for(P=n,k=0;k<L.length;k++){w=L[k];var ue=T[w],le=k===L.length-1;R=le?P/ue:Math.floor(P/ue),_[w]=R,P-=R*ue}if(m.round){var ee=B;for(k=0;k<L.length;k++)if(w=L[k],R=_[w],R!==0&&(ee--,ee===0)){for(var te=k+1;te<L.length;te++){var Z=L[te],ne=_[Z];_[w]+=ne*T[Z]/T[w],_[Z]=0}break}for(k=L.length-1;k>=0;k--)if(w=L[k],R=_[w],R!==0){var ot=Math.round(R);if(_[w]=ot,k===0)break;var ct=L[k-1],fn=T[ct],ut=Math.floor(ot*T[w]/fn);if(ut)_[ct]+=ut,_[w]=0;else break}}var $e=[];for(k=0;k<L.length&&$e.length<B;k++)w=L[k],R=_[w],R&&$e.push({unitName:w,unitCount:R});return $e}function z(n,m){var w=I(m);if(!n.length){var k=m.units,R=k[k.length-1];return j({unitName:R,unitCount:0},w,m)}var P=m.conjunction,L=m.serialComma,T;N(m,"delimiter")?T=m.delimiter:N(w,"delimiter")?T=w.delimiter:T=", ";for(var B=[],_=0;_<n.length;_++)B.push(j(n[_],w,m));return!P||n.length===1?B.join(T):n.length===2?B.join(P):B.slice(0,-1).join(T)+(L?",":"")+P+B.slice(-1)}function d(n){var m=function(k,R){k=Math.abs(k);var P=t({},m,R||{}),L=C(k,P);return z(L,P)};return t(m,{language:"en",spacer:" ",conjunction:"",serialComma:!0,units:["y","mo","w","d","h","m","s"],languages:{},round:!1,unitMeasures:{y:315576e5,mo:26298e5,w:6048e5,d:864e5,h:36e5,m:6e4,s:1e3,ms:1}},n)}var O=t(d({}),{getSupportedLanguages:function(){var m=[];for(var w in i)N(i,w)&&w!=="gr"&&m.push(w);return m},humanizer:d});e.exports?e.exports=O:this.humanizeDuration=O})()})(Fe)),Fe.exports}var Yi=Vi();const Et=Wn(Yi),Ui=[3600,28800,86400],ln=["push","mute"];function Xi(e){return _t({queryKey:ln,queryFn:async()=>(await Qe.get("/push/mute")).data,enabled:e,staleTime:Gn("1m")})}function Wi(){const e=Hn();return qn({mutationFn:t=>Qe.post("/push/mute",{durationSeconds:t}),onSuccess:()=>e.invalidateQueries({queryKey:ln})})}const Gi="h4JCaDns",Hi="J7YHjjGf",qi="OSxsHHFr",Ki="_7fxRRm-B",Ji="NqKyOtNo",re={bell:Gi,menu:Hi,title:qi,item:Ki,muted:Ji};function Qi(){const{isSubscribed:e}=Mr(),t=Xi(e),r=Wi();if(!e)return null;const a=t.data?.mutedForSeconds??0,i=a>0,s=o=>{Zn(o),r.mutate(o)};return c.jsx(Kn,{trigger:"click",interactive:!0,placement:"bottom-end",theme:"richup-blended",appendTo:()=>document.body,content:c.jsxs("div",{className:re.menu,children:[c.jsx("div",{className:re.title,children:"Game invite notifications"}),i?c.jsxs(c.Fragment,{children:[c.jsxs("span",{className:re.muted,children:["Muted for"," ",Et(a*1e3,{largest:1,round:!0})]}),c.jsx("button",{className:re.item,onClick:()=>s(0),children:"Unmute"})]}):Ui.map(o=>c.jsxs("button",{className:re.item,onClick:()=>s(o),children:["Mute for ",Et(o*1e3)]},o))]}),children:c.jsx("button",{className:re.bell,"aria-label":i?"Invite notifications muted":"Mute invite notifications",children:c.jsx(X,{icon:i?Jn:Qn})})})}const Zi="aibs05zY",eo="_4YYirDU9",to="HZ3x2FSX",no="iJKUZL6n",ro="_3-ISzsVr",ao="bBOJ6v7d",so="E4y4E5lI",io="c6uYyVyu",oo="VfduHAm9",co="pvk2axt1",uo="FNnsmX0T",lo="dpiKdp7X",fo="_5inoEREg",mo="CmfPBtNh",po="cSnjGOu-",ho="oS5-Tcx4",go="fUAkLGLm",yo="HqbbWVFd",$={lobbyContainer:Zi,lobby:eo,roomsListShown:to,logos:no,logo:ro,subtitle:ao,lobbyContents:so,actions:io,callToAction:oo,discordButton:co,public:"AOu--FWI",publicLoaderContents:uo,playMain:lo,shine:fo,private:"sCFZETMJ",roomButton:mo,instructions:po,topControls:ho,navBar:go,largerLoader:yo};function Ro({specificRoomId:e}){const{setShowVideoAd:t,maintenanceInfo:r}=v.useContext(Me),a=He(),i=Ar(),s=Js(e),[o,u]=v.useState(!1);return At(()=>e&&t(!0)),s?c.jsxs(Je,{className:[$.lobbyContainer,o&&$.roomsListShown],children:[c.jsxs("div",{className:$.lobby,style:{minHeight:i},children:[c.jsxs("div",{className:$.topControls,children:[c.jsx(Hr,{}),c.jsx(Qi,{}),!r?.isMaintenance&&c.jsx($i,{})]}),c.jsx(er,{showLogo:!1,className:$.navBar}),c.jsxs("div",{className:$.lobbyContents,children:[r?.isMaintenance===!1&&c.jsx(Li,{}),c.jsx(vo,{}),c.jsx(et,{isLoading:r===null||a.isPending,loader:c.jsx(So,{}),children:c.jsx(bo,{specificRoomId:e,isRoomsList:o,setIsRoomsList:u})})]}),c.jsx("div",{className:$.discordButton,children:c.jsx(tr,{from:"lobbyCorner"})})]}),c.jsx(nr,{}),c.jsx("div",{className:$.instructions,children:c.jsx(Hs,{animateIn:!0})}),c.jsx(rr,{})]}):c.jsx(Fi,{delayMs:500})}function vo(){const e=Ae(),a=ar().pathname==="/"?void 0:()=>e({to:"/"});return c.jsxs("div",{className:$.logos,children:[c.jsx(xo,{}),c.jsx(sr,{className:$.logo,onClick:a}),c.jsx("h2",{className:$.subtitle,children:"Rule the economy"})]})}function bo({specificRoomId:e,isRoomsList:t,setIsRoomsList:r}){const{name:a,maintenanceInfo:i,updateName:s}=v.useContext(Me),[o,u]=v.useState(a||""),[f,p]=v.useState(!1),[h,y]=v.useState(i?.isMaintenance),S=He();Rt(()=>{y(i?.isMaintenance)},[i?.isMaintenance]);function x(){s(f?o:qe(Mt,""))}return h?c.jsx(ui,{dismiss:()=>y(!1)}):t?c.jsx(vr,{onBack:()=>r(!1),beforeRedirect:x}):S.data?.bannedUntil?c.jsx(Bi,{until:S.data.bannedUntil}):c.jsxs(Je,{className:[$.actions,!1],children:[c.jsxs("div",{className:$.callToAction,children:[c.jsx($r,{onNameUpdated:b=>{u(b),p(!0)}}),c.jsx(ko,{specificRoomId:e,beforeRedirect:x})]}),c.jsx(wo,{beforeRedirect:x,onAllRoomsClick:()=>r(!0)})]})}function xo(){const[e,t]=v.useState(0);function r(){t(a=>a+1),Nr.dice.play()}return c.jsx(ir,{value:6,rollCount:e,onClick:r})}function ko({specificRoomId:e=null,beforeRedirect:t}){const[r,a]=v.useState(!1),i=Ae(),s=e!==null;async function o(){a(!0);const f=s?e:await br(mr.maxPlayers);await u(f),a(!1)}async function u(f){t(),await i({to:`/room/${f}`,state:{fromLobby:!0}})}return or("onContinuePlaying",f=>{u(f)}),c.jsx(et,{isLoading:r,className:$.public,contentClassName:$.publicLoaderContents,children:c.jsxs(se,{onClick:o,className:$.playMain,icon:c.jsx(X,{icon:cr}),noMargin:!0,children:[s?"Enter Game":"Play",c.jsx("div",{className:$.shine})]})})}function wo({beforeRedirect:e,onAllRoomsClick:t}){const r=Ae(),[a,i]=v.useState(!1);function s(u){e(),r({to:`/room/${u}`,state:{fromLobby:!0}})}async function o(){i(!0);try{const u=await xr(!0);s(u.roomId)}catch(u){fr(dr(u)),i(!1)}}return c.jsxs(et,{isLoading:a,className:$.private,contentClassName:$.privateContents,children:[c.jsx(se,{type:"subtle",className:$.roomButton,icon:c.jsx(X,{icon:ur}),onClick:t,children:"All rooms"}),c.jsx(se,{onClick:o,className:$.roomButton,type:"subtle",icon:c.jsx(X,{icon:lr}),children:"Create a private game"})]})}function So(){return c.jsx(X,{icon:hr,spin:!0,className:$.largerLoader})}export{li as D,Hs as G,Ro as L,$i as W,Fi as a,Xr as b,Ur as c,Hr as d,Et as h,Ks as u};
