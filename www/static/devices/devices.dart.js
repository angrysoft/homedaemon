{}(function dartProgram(){function copyProperties(a,b){var u=Object.keys(a)
for(var t=0;t<u.length;t++){var s=u[t]
b[s]=a[s]}}var z=function(){var u=function(){}
u.prototype={p:{}}
var t=new u()
if(!(t.__proto__&&t.__proto__.p===u.prototype.p))return false
try{if(typeof navigator!="undefined"&&typeof navigator.userAgent=="string"&&navigator.userAgent.indexOf("Chrome/")>=0)return true
if(typeof version=="function"&&version.length==0){var s=version()
if(/^\d+\.\d+\.\d+\.\d+$/.test(s))return true}}catch(r){}return false}()
function setFunctionNamesIfNecessary(a){function t(){};if(typeof t.name=="string")return
for(var u=0;u<a.length;u++){var t=a[u]
var s=Object.keys(t)
for(var r=0;r<s.length;r++){var q=s[r]
var p=t[q]
if(typeof p=='function')p.name=q}}}function inherit(a,b){a.prototype.constructor=a
a.prototype["$i"+a.name]=a
if(b!=null){if(z){a.prototype.__proto__=b.prototype
return}var u=Object.create(b.prototype)
copyProperties(a.prototype,u)
a.prototype=u}}function inheritMany(a,b){for(var u=0;u<b.length;u++)inherit(b[u],a)}function mixin(a,b){copyProperties(b.prototype,a.prototype)
a.prototype.constructor=a}function lazy(a,b,c,d){var u=a
a[b]=u
a[c]=function(){a[c]=function(){H.d6(b)}
var t
var s=d
try{if(a[b]===u){t=a[b]=s
t=a[b]=d()}else t=a[b]}finally{if(t===s)a[b]=null
a[c]=function(){return this[b]}}return t}}function makeConstList(a){a.immutable$list=Array
a.fixed$length=Array
return a}function convertToFastObject(a){function t(){}t.prototype=a
new t()
return a}function convertAllToFastObject(a){for(var u=0;u<a.length;++u)convertToFastObject(a[u])}var y=0
function tearOffGetter(a,b,c,d,e){return e?new Function("funcs","applyTrampolineIndex","reflectionInfo","name","H","c","return function tearOff_"+d+y+++"(receiver) {"+"if (c === null) c = "+"H.by"+"("+"this, funcs, applyTrampolineIndex, reflectionInfo, false, true, name);"+"return new c(this, funcs[0], receiver, name);"+"}")(a,b,c,d,H,null):new Function("funcs","applyTrampolineIndex","reflectionInfo","name","H","c","return function tearOff_"+d+y+++"() {"+"if (c === null) c = "+"H.by"+"("+"this, funcs, applyTrampolineIndex, reflectionInfo, false, false, name);"+"return new c(this, funcs[0], null, name);"+"}")(a,b,c,d,H,null)}function tearOff(a,b,c,d,e,f){var u=null
return d?function(){if(u===null)u=H.by(this,a,b,c,true,false,e).prototype
return u}:tearOffGetter(a,b,c,e,f)}var x=0
function installTearOff(a,b,c,d,e,f,g,h,i,j){var u=[]
for(var t=0;t<h.length;t++){var s=h[t]
if(typeof s=='string')s=a[s]
s.$callName=g[t]
u.push(s)}var s=u[0]
s.$R=e
s.$D=f
var r=i
if(typeof r=="number")r+=x
var q=h[0]
s.$stubName=q
var p=tearOff(u,j||0,r,c,q,d)
a[b]=p
if(c)s.$tearOff=p}function installStaticTearOff(a,b,c,d,e,f,g,h){return installTearOff(a,b,true,false,c,d,e,f,g,h)}function installInstanceTearOff(a,b,c,d,e,f,g,h,i){return installTearOff(a,b,false,c,d,e,f,g,h,i)}function setOrUpdateInterceptorsByTag(a){var u=v.interceptorsByTag
if(!u){v.interceptorsByTag=a
return}copyProperties(a,u)}function setOrUpdateLeafTags(a){var u=v.leafTags
if(!u){v.leafTags=a
return}copyProperties(a,u)}function updateTypes(a){var u=v.types
var t=u.length
u.push.apply(u,a)
return t}function updateHolder(a,b){copyProperties(b,a)
return a}var hunkHelpers=function(){var u=function(a,b,c,d,e){return function(f,g,h,i){return installInstanceTearOff(f,g,a,b,c,d,[h],i,e)}},t=function(a,b,c,d){return function(e,f,g,h){return installStaticTearOff(e,f,a,b,c,[g],h,d)}}
return{inherit:inherit,inheritMany:inheritMany,mixin:mixin,installStaticTearOff:installStaticTearOff,installInstanceTearOff:installInstanceTearOff,_instance_0u:u(0,0,null,["$0"],0),_instance_1u:u(0,1,null,["$1"],0),_instance_2u:u(0,2,null,["$2"],0),_instance_0i:u(1,0,null,["$0"],0),_instance_1i:u(1,1,null,["$1"],0),_instance_2i:u(1,2,null,["$2"],0),_static_0:t(0,null,["$0"],0),_static_1:t(1,null,["$1"],0),_static_2:t(2,null,["$2"],0),makeConstList:makeConstList,lazy:lazy,updateHolder:updateHolder,convertToFastObject:convertToFastObject,setFunctionNamesIfNecessary:setFunctionNamesIfNecessary,updateTypes:updateTypes,setOrUpdateInterceptorsByTag:setOrUpdateInterceptorsByTag,setOrUpdateLeafTags:setOrUpdateLeafTags}}()
function initializeDeferredHunk(a){x=v.types.length
a(hunkHelpers,v,w,$)}function getGlobalFromName(a){for(var u=0;u<w.length;u++){if(w[u]==C)continue
if(w[u][a])return w[u][a]}}var C={},H={bq:function bq(){},
L:function(a){var u,t=H.d7(a)
if(typeof t==="string")return t
u="minified:"+a
return u},
cU:function(a){return v.types[H.K(a)]},
a:function(a){var u
if(typeof a==="string")return a
if(typeof a==="number"){if(a!==0)return""+a}else if(!0===a)return"true"
else if(!1===a)return"false"
else if(a==null)return"null"
u=J.ae(a)
if(typeof u!=="string")throw H.b(H.cK(a))
return u},
a4:function(a){return H.cn(a)+H.bv(H.X(a),0,null)},
cn:function(a){var u,t,s,r,q,p,o,n,m=null,l=J.q(a),k=l.constructor
if(typeof k=="function"){u=k.name
t=typeof u==="string"?u:m}else t=m
s=t==null
if(s||l===C.o||!!l.$iR){r=C.c(a)
if(s)t=r
if(r==="Object"){q=a.constructor
if(typeof q=="function"){p=String(q).match(/^\s*function\s*([\w$]*)\s*\(/)
o=p==null?m:p[1]
if(typeof o==="string"&&/^\w+$/.test(o))t=o}}return t}t=t
n=t.length
if(n>1&&C.f.P(t,0)===36){if(1>n)H.ad(P.bs(1,m))
if(n>n)H.ad(P.bs(n,m))
t=t.substring(1,n)}return H.L(t)},
bA:function(a,b){if(a==null)J.bF(a)
throw H.b(H.bX(a,b))},
bX:function(a,b){var u,t="index"
if(typeof b!=="number"||Math.floor(b)!==b)return new P.w(!0,b,t,null)
u=J.bF(a)
if(b<0||b>=u)return new P.am(u,!0,b,t,"Index out of range")
return P.bs(b,t)},
cK:function(a){return new P.w(!0,a,null,null)},
b:function(a){var u
if(a==null)a=new P.Q()
u=new Error()
u.dartException=a
if("defineProperty" in Object){Object.defineProperty(u,"message",{get:H.c3})
u.name=""}else u.toString=H.c3
return u},
c3:function(){return J.ae(this.dartException)},
ad:function(a){throw H.b(a)},
d5:function(a){throw H.b(new P.ai(a))},
v:function(a){var u,t,s,r,q,p
a=H.d3(a.replace(String({}),'$receiver$'))
u=a.match(/\\\$[a-zA-Z]+\\\$/g)
if(u==null)u=H.bC([],[P.r])
t=u.indexOf("\\$arguments\\$")
s=u.indexOf("\\$argumentsExpr\\$")
r=u.indexOf("\\$expr\\$")
q=u.indexOf("\\$method\\$")
p=u.indexOf("\\$receiver\\$")
return new H.aA(a.replace(new RegExp('\\\\\\$arguments\\\\\\$','g'),'((?:x|[^x])*)').replace(new RegExp('\\\\\\$argumentsExpr\\\\\\$','g'),'((?:x|[^x])*)').replace(new RegExp('\\\\\\$expr\\\\\\$','g'),'((?:x|[^x])*)').replace(new RegExp('\\\\\\$method\\\\\\$','g'),'((?:x|[^x])*)').replace(new RegExp('\\\\\\$receiver\\\\\\$','g'),'((?:x|[^x])*)'),t,s,r,q,p)},
aB:function(a){return function($expr$){var $argumentsExpr$='$arguments$'
try{$expr$.$method$($argumentsExpr$)}catch(u){return u.message}}(a)},
bN:function(a){return function($expr$){try{$expr$.$method$}catch(u){return u.message}}(a)},
bL:function(a,b){return new H.at(a,b==null?null:b.method)},
br:function(a,b){var u=b==null,t=u?null:b.method
return new H.ar(a,t,u?null:b.receiver)},
a_:function(a){var u,t,s,r,q,p,o,n,m,l,k,j,i,h,g=null,f=new H.bm(a)
if(a==null)return
if(a instanceof H.O)return f.$1(a.a)
if(typeof a!=="object")return a
if("dartException" in a)return f.$1(a.dartException)
else if(!("message" in a))return a
u=a.message
if("number" in a&&typeof a.number=="number"){t=a.number
s=t&65535
if((C.p.S(t,16)&8191)===10)switch(s){case 438:return f.$1(H.br(H.a(u)+" (Error "+s+")",g))
case 445:case 5007:return f.$1(H.bL(H.a(u)+" (Error "+s+")",g))}}if(a instanceof TypeError){r=$.c5()
q=$.c6()
p=$.c7()
o=$.c8()
n=$.cb()
m=$.cc()
l=$.ca()
$.c9()
k=$.ce()
j=$.cd()
i=r.i(u)
if(i!=null)return f.$1(H.br(H.B(u),i))
else{i=q.i(u)
if(i!=null){i.method="call"
return f.$1(H.br(H.B(u),i))}else{i=p.i(u)
if(i==null){i=o.i(u)
if(i==null){i=n.i(u)
if(i==null){i=m.i(u)
if(i==null){i=l.i(u)
if(i==null){i=o.i(u)
if(i==null){i=k.i(u)
if(i==null){i=j.i(u)
h=i!=null}else h=!0}else h=!0}else h=!0}else h=!0}else h=!0}else h=!0}else h=!0
if(h)return f.$1(H.bL(H.B(u),i))}}return f.$1(new H.aE(typeof u==="string"?u:""))}if(a instanceof RangeError){if(typeof u==="string"&&u.indexOf("call stack")!==-1)return new P.a6()
u=function(b){try{return String(b)}catch(e){}return null}(a)
return f.$1(new P.w(!1,g,g,typeof u==="string"?u.replace(/^RangeError:\s*/,""):u))}if(typeof InternalError=="function"&&a instanceof InternalError)if(typeof u==="string"&&u==="too much recursion")return new P.a6()
return a},
Y:function(a){var u
if(a instanceof H.O)return a.b
if(a==null)return new H.a9(a)
u=a.$cachedTrace
if(u!=null)return u
return a.$cachedTrace=new H.a9(a)},
cY:function(a,b,c,d,e,f){H.h(a,"$ibo")
switch(H.K(b)){case 0:return a.$0()
case 1:return a.$1(c)
case 2:return a.$2(c,d)
case 3:return a.$3(c,d,e)
case 4:return a.$4(c,d,e,f)}throw H.b(new P.aO("Unsupported number of arguments for wrapped closure"))},
W:function(a,b){var u=a.$identity
if(!!u)return u
u=function(c,d,e){return function(f,g,h,i){return e(c,d,f,g,h,i)}}(a,b,H.cY)
a.$identity=u
return u},
cj:function(a,b,c,d,e,f,g){var u,t,s,r,q,p,o,n,m=null,l=b[0],k=l.$callName,j=e?Object.create(new H.ay().constructor.prototype):Object.create(new H.a0(m,m,m,m).constructor.prototype)
j.$initialize=j.constructor
if(e)u=function static_tear_off(){this.$initialize()}
else{t=$.u
if(typeof t!=="number")return t.j()
$.u=t+1
t=new Function("a,b,c,d"+t,"this.$initialize(a,b,c,d"+t+")")
u=t}j.constructor=u
u.prototype=j
if(!e){s=H.bJ(a,l,f)
s.$reflectionInfo=d}else{j.$static_name=g
s=l}r=H.cf(d,e,f)
j.$S=r
j[k]=s
for(q=s,p=1;p<b.length;++p){o=b[p]
n=o.$callName
if(n!=null){o=e?o:H.bJ(a,o,f)
j[n]=o}if(p===c){o.$reflectionInfo=d
q=o}}j.$C=q
j.$R=l.$R
j.$D=l.$D
return u},
cf:function(a,b,c){var u
if(typeof a=="number")return function(d,e){return function(){return d(e)}}(H.cU,a)
if(typeof a=="function")if(b)return a
else{u=c?H.bI:H.bn
return function(d,e){return function(){return d.apply({$receiver:e(this)},arguments)}}(a,u)}throw H.b("Error in functionType of tearoff")},
cg:function(a,b,c,d){var u=H.bn
switch(b?-1:a){case 0:return function(e,f){return function(){return f(this)[e]()}}(c,u)
case 1:return function(e,f){return function(g){return f(this)[e](g)}}(c,u)
case 2:return function(e,f){return function(g,h){return f(this)[e](g,h)}}(c,u)
case 3:return function(e,f){return function(g,h,i){return f(this)[e](g,h,i)}}(c,u)
case 4:return function(e,f){return function(g,h,i,j){return f(this)[e](g,h,i,j)}}(c,u)
case 5:return function(e,f){return function(g,h,i,j,k){return f(this)[e](g,h,i,j,k)}}(c,u)
default:return function(e,f){return function(){return e.apply(f(this),arguments)}}(d,u)}},
bJ:function(a,b,c){var u,t,s,r,q,p,o
if(c)return H.ci(a,b)
u=b.$stubName
t=b.length
s=a[u]
r=b==null?s==null:b===s
q=!r||t>=27
if(q)return H.cg(t,!r,u,b)
if(t===0){r=$.u
if(typeof r!=="number")return r.j()
$.u=r+1
p="self"+r
r="return function(){var "+p+" = this."
q=$.M
return new Function(r+H.a(q==null?$.M=H.ah("self"):q)+";return "+p+"."+H.a(u)+"();}")()}o="abcdefghijklmnopqrstuvwxyz".split("").splice(0,t).join(",")
r=$.u
if(typeof r!=="number")return r.j()
$.u=r+1
o+=r
r="return function("+o+"){return this."
q=$.M
return new Function(r+H.a(q==null?$.M=H.ah("self"):q)+"."+H.a(u)+"("+o+");}")()},
ch:function(a,b,c,d){var u=H.bn,t=H.bI
switch(b?-1:a){case 0:throw H.b(new H.aw("Intercepted function with no arguments."))
case 1:return function(e,f,g){return function(){return f(this)[e](g(this))}}(c,u,t)
case 2:return function(e,f,g){return function(h){return f(this)[e](g(this),h)}}(c,u,t)
case 3:return function(e,f,g){return function(h,i){return f(this)[e](g(this),h,i)}}(c,u,t)
case 4:return function(e,f,g){return function(h,i,j){return f(this)[e](g(this),h,i,j)}}(c,u,t)
case 5:return function(e,f,g){return function(h,i,j,k){return f(this)[e](g(this),h,i,j,k)}}(c,u,t)
case 6:return function(e,f,g){return function(h,i,j,k,l){return f(this)[e](g(this),h,i,j,k,l)}}(c,u,t)
default:return function(e,f,g,h){return function(){h=[g(this)]
Array.prototype.push.apply(h,arguments)
return e.apply(f(this),h)}}(d,u,t)}},
ci:function(a,b){var u,t,s,r,q,p,o,n=$.M
if(n==null)n=$.M=H.ah("self")
u=$.bH
if(u==null)u=$.bH=H.ah("receiver")
t=b.$stubName
s=b.length
r=a[t]
q=b==null?r==null:b===r
p=!q||s>=28
if(p)return H.ch(s,!q,t,b)
if(s===1){n="return function(){return this."+H.a(n)+"."+H.a(t)+"(this."+H.a(u)+");"
u=$.u
if(typeof u!=="number")return u.j()
$.u=u+1
return new Function(n+u+"}")()}o="abcdefghijklmnopqrstuvwxyz".split("").splice(0,s-1).join(",")
n="return function("+o+"){return this."+H.a(n)+"."+H.a(t)+"(this."+H.a(u)+", "+o+");"
u=$.u
if(typeof u!=="number")return u.j()
$.u=u+1
return new Function(n+u+"}")()},
by:function(a,b,c,d,e,f,g){return H.cj(a,b,c,d,!!e,!!f,g)},
bn:function(a){return a.a},
bI:function(a){return a.c},
ah:function(a){var u,t,s,r=new H.a0("self","target","receiver","name"),q=J.bK(Object.getOwnPropertyNames(r))
for(u=q.length,t=0;t<u;++t){s=q[t]
if(r[s]===a)return s}},
cQ:function(a){if(a==null)H.cM("boolean expression must not be null")
return a},
B:function(a){if(a==null)return a
if(typeof a==="string")return a
throw H.b(H.y(a,"String"))},
dp:function(a){if(a==null)return a
if(typeof a==="boolean")return a
throw H.b(H.y(a,"bool"))},
K:function(a){if(a==null)return a
if(typeof a==="number"&&Math.floor(a)===a)return a
throw H.b(H.y(a,"int"))},
d2:function(a,b){throw H.b(H.y(a,H.L(H.B(b).substring(2))))},
h:function(a,b){if(a==null)return a
if((typeof a==="object"||typeof a==="function")&&J.q(a)[b])return a
H.d2(a,b)},
bY:function(a){var u
if("$S" in a){u=a.$S
if(typeof u=="number")return v.types[H.K(u)]
else return a.$S()}return},
aa:function(a,b){var u
if(typeof a=="function")return!0
u=H.bY(J.q(a))
if(u==null)return!1
return H.bR(u,null,b,null)},
c:function(a,b){var u,t
if(a==null)return a
if($.bt)return a
$.bt=!0
try{if(H.aa(a,b))return a
u=H.bl(b)
t=H.y(a,u)
throw H.b(t)}finally{$.bt=!1}},
J:function(a,b){if(a!=null&&!H.bx(a,b))H.ad(H.y(a,H.bl(b)))
return a},
y:function(a,b){return new H.aC("TypeError: "+P.al(a)+": type '"+H.a(H.cI(a))+"' is not a subtype of type '"+b+"'")},
cI:function(a){var u,t=J.q(a)
if(!!t.$iN){u=H.bY(t)
if(u!=null)return H.bl(u)
return"Closure"}return H.a4(a)},
cM:function(a){throw H.b(new H.aG(a))},
d6:function(a){throw H.b(new P.aj(a))},
bZ:function(a){return v.getIsolateTag(a)},
bC:function(a,b){a.$ti=b
return a},
X:function(a){if(a==null)return
return a.$ti},
dr:function(a,b,c){return H.ac(a["$a"+H.a(c)],H.X(b))},
m:function(a,b){var u=H.X(a)
return u==null?null:u[b]},
bl:function(a){return H.z(a,null)},
z:function(a,b){var u,t
if(a==null)return"dynamic"
if(a===-1)return"void"
if(typeof a==="object"&&a!==null&&a.constructor===Array)return H.L(a[0].name)+H.bv(a,1,b)
if(typeof a=="function")return H.L(a.name)
if(a===-2)return"dynamic"
if(typeof a==="number"){H.K(a)
if(b==null||a<0||a>=b.length)return"unexpected-generic-index:"+a
u=b.length
t=u-a-1
if(t<0||t>=u)return H.bA(b,t)
return H.a(b[t])}if('func' in a)return H.cz(a,b)
if('futureOr' in a)return"FutureOr<"+H.z("type" in a?a.type:null,b)+">"
return"unknown-reified-type"},
cz:function(a,a0){var u,t,s,r,q,p,o,n,m,l,k,j,i,h,g,f,e,d,c,b=", "
if("bounds" in a){u=a.bounds
if(a0==null){a0=H.bC([],[P.r])
t=null}else t=a0.length
s=a0.length
for(r=u.length,q=r;q>0;--q)C.e.I(a0,"T"+(s+q))
for(p="<",o="",q=0;q<r;++q,o=b){p+=o
n=a0.length
m=n-q-1
if(m<0)return H.bA(a0,m)
p=C.f.j(p,a0[m])
l=u[q]
if(l!=null&&l!==P.e)p+=" extends "+H.z(l,a0)}p+=">"}else{p=""
t=null}k=!!a.v?"void":H.z(a.ret,a0)
if("args" in a){j=a.args
for(n=j.length,i="",h="",g=0;g<n;++g,h=b){f=j[g]
i=i+h+H.z(f,a0)}}else{i=""
h=""}if("opt" in a){e=a.opt
i+=h+"["
for(n=e.length,h="",g=0;g<n;++g,h=b){f=e[g]
i=i+h+H.z(f,a0)}i+="]"}if("named" in a){d=a.named
i+=h+"{"
for(n=H.cR(d),m=n.length,h="",g=0;g<m;++g,h=b){c=H.B(n[g])
i=i+h+H.z(d[c],a0)+(" "+H.a(c))}i+="}"}if(t!=null)a0.length=t
return p+"("+i+") => "+k},
bv:function(a,b,c){var u,t,s,r,q,p
if(a==null)return""
u=new P.a7("")
for(t=b,s="",r=!0,q="";t<a.length;++t,s=", "){u.a=q+s
p=a[t]
if(p!=null)r=!1
q=u.a+=H.z(p,c)}return"<"+u.h(0)+">"},
ac:function(a,b){if(a==null)return b
a=a.apply(null,b)
if(a==null)return
if(typeof a==="object"&&a!==null&&a.constructor===Array)return a
if(typeof a=="function")return a.apply(null,b)
return b},
V:function(a,b,c,d){var u,t
if(a==null)return!1
u=H.X(a)
t=J.q(a)
if(t[b]==null)return!1
return H.bV(H.ac(t[d],u),null,c,null)},
cL:function(a,b,c,d){if(a==null)return a
if(H.V(a,b,c,d))return a
throw H.b(H.y(a,function(e,f){return e.replace(/[^<,> ]+/g,function(g){return f[g]||g})}(H.L(b.substring(2))+H.bv(c,0,null),v.mangledGlobalNames)))},
bV:function(a,b,c,d){var u,t
if(c==null)return!0
if(a==null){u=c.length
for(t=0;t<u;++t)if(!H.o(null,null,c[t],d))return!1
return!0}u=a.length
for(t=0;t<u;++t)if(!H.o(a[t],b,c[t],d))return!1
return!0},
dq:function(a,b,c){return a.apply(b,H.ac(J.q(b)["$a"+H.a(c)],H.X(b)))},
c0:function(a){var u
if(typeof a==="number")return!1
if('futureOr' in a){u="type" in a?a.type:null
return a==null||a.name==="e"||a.name==="f"||a===-1||a===-2||H.c0(u)}return!1},
bx:function(a,b){var u,t
if(a==null)return b==null||b.name==="e"||b.name==="f"||b===-1||b===-2||H.c0(b)
if(b==null||b===-1||b.name==="e"||b===-2)return!0
if(typeof b=="object"){if('futureOr' in b)if(H.bx(a,"type" in b?b.type:null))return!0
if('func' in b)return H.aa(a,b)}u=J.q(a).constructor
t=H.X(a)
if(t!=null){t=t.slice()
t.splice(0,0,u)
u=t}return H.o(u,null,b,null)},
p:function(a,b){if(a!=null&&!H.bx(a,b))throw H.b(H.y(a,H.bl(b)))
return a},
o:function(a,b,c,d){var u,t,s,r,q,p,o,n,m,l=null
if(a===c)return!0
if(c==null||c===-1||c.name==="e"||c===-2)return!0
if(a===-2)return!0
if(a==null||a===-1||a.name==="e"||a===-2){if(typeof c==="number")return!1
if('futureOr' in c)return H.o(a,b,"type" in c?c.type:l,d)
return!1}if(typeof a==="number")return H.o(b[H.K(a)],b,c,d)
if(typeof c==="number")return!1
if(a.name==="f")return!0
u=typeof a==="object"&&a!==null&&a.constructor===Array
t=u?a[0]:a
if('futureOr' in c){s="type" in c?c.type:l
if('futureOr' in a)return H.o("type" in a?a.type:l,b,s,d)
else if(H.o(a,b,s,d))return!0
else{if(!('$i'+"n" in t.prototype))return!1
r=t.prototype["$a"+"n"]
q=H.ac(r,u?a.slice(1):l)
return H.o(typeof q==="object"&&q!==null&&q.constructor===Array?q[0]:l,b,s,d)}}if('func' in c)return H.bR(a,b,c,d)
if('func' in a)return c.name==="bo"
p=typeof c==="object"&&c!==null&&c.constructor===Array
o=p?c[0]:c
if(o!==t){n=o.name
if(!('$i'+n in t.prototype))return!1
m=t.prototype["$a"+n]}else m=l
if(!p)return!0
u=u?a.slice(1):l
p=c.slice(1)
return H.bV(H.ac(m,u),b,p,d)},
bR:function(a,b,c,d){var u,t,s,r,q,p,o,n,m,l,k,j,i,h,g
if(!('func' in a))return!1
if("bounds" in a){if(!("bounds" in c))return!1
u=a.bounds
t=c.bounds
if(u.length!==t.length)return!1
b=b==null?u:u.concat(b)
d=d==null?t:t.concat(d)}else if("bounds" in c)return!1
if(!H.o(a.ret,b,c.ret,d))return!1
s=a.args
r=c.args
q=a.opt
p=c.opt
o=s!=null?s.length:0
n=r!=null?r.length:0
m=q!=null?q.length:0
l=p!=null?p.length:0
if(o>n)return!1
if(o+m<n+l)return!1
for(k=0;k<o;++k)if(!H.o(r[k],d,s[k],b))return!1
for(j=k,i=0;j<n;++i,++j)if(!H.o(r[j],d,q[i],b))return!1
for(j=0;j<l;++i,++j)if(!H.o(p[j],d,q[i],b))return!1
h=a.named
g=c.named
if(g==null)return!0
if(h==null)return!1
return H.d0(h,b,g,d)},
d0:function(a,b,c,d){var u,t,s,r=Object.getOwnPropertyNames(c)
for(u=r.length,t=0;t<u;++t){s=r[t]
if(!Object.hasOwnProperty.call(a,s))return!1
if(!H.o(c[s],d,a[s],b))return!1}return!0},
cZ:function(a){var u,t,s,r,q=H.B($.c_.$1(a)),p=$.bc[q]
if(p!=null){Object.defineProperty(a,v.dispatchPropertyName,{value:p,enumerable:false,writable:true,configurable:true})
return p.i}u=$.bh[q]
if(u!=null)return u
t=v.interceptorsByTag[q]
if(t==null){q=H.B($.bU.$2(a,q))
if(q!=null){p=$.bc[q]
if(p!=null){Object.defineProperty(a,v.dispatchPropertyName,{value:p,enumerable:false,writable:true,configurable:true})
return p.i}u=$.bh[q]
if(u!=null)return u
t=v.interceptorsByTag[q]}}if(t==null)return
u=t.prototype
s=q[0]
if(s==="!"){p=H.bi(u)
$.bc[q]=p
Object.defineProperty(a,v.dispatchPropertyName,{value:p,enumerable:false,writable:true,configurable:true})
return p.i}if(s==="~"){$.bh[q]=u
return u}if(s==="-"){r=H.bi(u)
Object.defineProperty(Object.getPrototypeOf(a),v.dispatchPropertyName,{value:r,enumerable:false,writable:true,configurable:true})
return r.i}if(s==="+")return H.c1(a,u)
if(s==="*")throw H.b(P.bO(q))
if(v.leafTags[q]===true){r=H.bi(u)
Object.defineProperty(Object.getPrototypeOf(a),v.dispatchPropertyName,{value:r,enumerable:false,writable:true,configurable:true})
return r.i}else return H.c1(a,u)},
c1:function(a,b){var u=Object.getPrototypeOf(a)
Object.defineProperty(u,v.dispatchPropertyName,{value:J.bB(b,u,null,null),enumerable:false,writable:true,configurable:true})
return b},
bi:function(a){return J.bB(a,!1,null,!!a.$ida)},
d_:function(a,b,c){var u=b.prototype
if(v.leafTags[a]===true)return H.bi(u)
else return J.bB(u,c,null,null)},
cW:function(){if(!0===$.bz)return
$.bz=!0
H.cX()},
cX:function(){var u,t,s,r,q,p,o,n
$.bc=Object.create(null)
$.bh=Object.create(null)
H.cV()
u=v.interceptorsByTag
t=Object.getOwnPropertyNames(u)
if(typeof window!="undefined"){window
s=function(){}
for(r=0;r<t.length;++r){q=t[r]
p=$.c2.$1(q)
if(p!=null){o=H.d_(q,u[q],p)
if(o!=null){Object.defineProperty(p,v.dispatchPropertyName,{value:o,enumerable:false,writable:true,configurable:true})
s.prototype=p}}}}for(r=0;r<t.length;++r){q=t[r]
if(/^[A-Za-z_]/.test(q)){n=u[q]
u["!"+q]=n
u["~"+q]=n
u["-"+q]=n
u["+"+q]=n
u["*"+q]=n}}},
cV:function(){var u,t,s,r,q,p,o=C.i()
o=H.H(C.j,H.H(C.k,H.H(C.d,H.H(C.d,H.H(C.l,H.H(C.m,H.H(C.n(C.c),o)))))))
if(typeof dartNativeDispatchHooksTransformer!="undefined"){u=dartNativeDispatchHooksTransformer
if(typeof u=="function")u=[u]
if(u.constructor==Array)for(t=0;t<u.length;++t){s=u[t]
if(typeof s=="function")o=s(o)||o}}r=o.getTag
q=o.getUnknownTag
p=o.prototypeForTag
$.c_=new H.be(r)
$.bU=new H.bf(q)
$.c2=new H.bg(p)},
H:function(a,b){return a(b)||b},
d3:function(a){if(/[[\]{}()*+?.\\^$|]/.test(a))return a.replace(/[[\]{}()*+?.\\^$|]/g,"\\$&")
return a},
aA:function aA(a,b,c,d,e,f){var _=this
_.a=a
_.b=b
_.c=c
_.d=d
_.e=e
_.f=f},
at:function at(a,b){this.a=a
this.b=b},
ar:function ar(a,b,c){this.a=a
this.b=b
this.c=c},
aE:function aE(a){this.a=a},
O:function O(a,b){this.a=a
this.b=b},
bm:function bm(a){this.a=a},
a9:function a9(a){this.a=a
this.b=null},
N:function N(){},
az:function az(){},
ay:function ay(){},
a0:function a0(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.d=d},
aC:function aC(a){this.a=a},
aw:function aw(a){this.a=a},
aG:function aG(a){this.a=a},
be:function be(a){this.a=a},
bf:function bf(a){this.a=a},
bg:function bg(a){this.a=a},
cR:function(a){return J.bK(H.bC(a?Object.keys(a):[],[null]))},
d7:function(a){return v.mangledGlobalNames[a]}},J={
bB:function(a,b,c,d){return{i:a,p:b,e:c,x:d}},
cT:function(a){var u,t,s,r,q=a[v.dispatchPropertyName]
if(q==null)if($.bz==null){H.cW()
q=a[v.dispatchPropertyName]}if(q!=null){u=q.p
if(!1===u)return q.i
if(!0===u)return a
t=Object.getPrototypeOf(a)
if(u===t)return q.i
if(q.e===t)throw H.b(P.bO("Return interceptor for "+H.a(u(a,q))))}s=a.constructor
r=s==null?null:s[$.bD()]
if(r!=null)return r
r=H.cZ(a)
if(r!=null)return r
if(typeof a=="function")return C.q
u=Object.getPrototypeOf(a)
if(u==null)return C.h
if(u===Object.prototype)return C.h
if(typeof s=="function"){Object.defineProperty(s,$.bD(),{value:C.b,enumerable:false,writable:true,configurable:true})
return C.b}return C.b},
bK:function(a){a.fixed$length=Array
return a},
q:function(a){if(typeof a=="number"){if(Math.floor(a)==a)return J.a1.prototype
return J.ao.prototype}if(typeof a=="string")return J.P.prototype
if(a==null)return J.ap.prototype
if(typeof a=="boolean")return J.an.prototype
if(a.constructor==Array)return J.D.prototype
if(typeof a!="object"){if(typeof a=="function")return J.a2.prototype
return a}if(a instanceof P.e)return a
return J.cT(a)},
cS:function(a){if(typeof a=="string")return J.P.prototype
if(a==null)return a
if(a.constructor==Array)return J.D.prototype
if(!(a instanceof P.e))return J.R.prototype
return a},
bF:function(a){return J.cS(a).gn(a)},
ae:function(a){return J.q(a).h(a)},
i:function i(){},
an:function an(){},
ap:function ap(){},
a3:function a3(){},
au:function au(){},
R:function R(){},
a2:function a2(){},
D:function D(a){this.$ti=a},
bp:function bp(a){this.$ti=a},
af:function af(a,b,c){var _=this
_.a=a
_.b=b
_.c=0
_.d=null
_.$ti=c},
aq:function aq(){},
a1:function a1(){},
ao:function ao(){},
P:function P(){}},P={
cp:function(){var u,t,s={}
if(self.scheduleImmediate!=null)return P.cN()
if(self.MutationObserver!=null&&self.document!=null){u=self.document.createElement("div")
t=self.document.createElement("span")
s.a=null
new self.MutationObserver(H.W(new P.aK(s),1)).observe(u,{childList:true})
return new P.aJ(s,u,t)}else if(self.setImmediate!=null)return P.cO()
return P.cP()},
cq:function(a){self.scheduleImmediate(H.W(new P.aL(H.c(a,{func:1,ret:-1})),0))},
cr:function(a){self.setImmediate(H.W(new P.aM(H.c(a,{func:1,ret:-1})),0))},
cs:function(a){H.c(a,{func:1,ret:-1})
P.ct(0,a)},
ct:function(a,b){var u=new P.b5()
u.N(a,b)
return u},
cB:function(a){return new P.aH(new P.j($.d,[a]),[a])},
cx:function(a,b){a.$2(0,null)
b.b=!0
return b.a},
cu:function(a,b){P.cy(a,b)},
cw:function(a,b){b.u(a)},
cv:function(a,b){b.v(H.a_(a),H.Y(a))},
cy:function(a,b){var u,t=null,s=new P.b8(b),r=new P.b9(b),q=J.q(a)
if(!!q.$ij)a.H(s,r,t)
else if(!!q.$in)a.B(s,r,t)
else{u=new P.j($.d,[null])
H.p(a,null)
u.a=4
u.c=a
u.H(s,t,t)}},
cJ:function(a){var u=function(b,c){return function(d,e){while(true)try{b(d,e)
break}catch(t){e=t
d=c}}}(a,1)
return $.d.K(new P.bb(u),P.f,P.A,null)},
bQ:function(a,b){var u,t,s
b.a=1
try{a.B(new P.aT(b),new P.aU(b),P.f)}catch(s){u=H.a_(s)
t=H.Y(s)
P.d4(new P.aV(b,u,t))}},
aS:function(a,b){var u,t
for(;u=a.a,u===2;)a=H.h(a.c,"$ij")
if(u>=4){t=b.l()
b.a=a.a
b.c=a.c
P.E(b,t)}else{t=H.h(b.c,"$it")
b.a=2
b.c=a
a.G(t)}},
E:function(a,b){var u,t,s,r,q,p,o,n,m,l,k,j,i=null,h={},g=h.a=a
for(;!0;){u={}
t=g.a===8
if(b==null){if(t){s=H.h(g.c,"$il")
P.bw(i,i,g.b,s.a,s.b)}return}for(;r=b.a,r!=null;b=r){b.a=null
P.E(h.a,b)}g=h.a
q=g.c
u.a=t
u.b=q
p=!t
if(p){o=b.c
o=(o&1)!==0||(o&15)===8}else o=!0
if(o){o=b.b
n=o.b
if(t){m=g.b===n
m=!(m||m)}else m=!1
if(m){H.h(q,"$il")
P.bw(i,i,g.b,q.a,q.b)
return}l=$.d
if(l!==n)$.d=n
else l=i
g=b.c
if((g&15)===8)new P.b_(h,u,b,t).$0()
else if(p){if((g&1)!==0)new P.aZ(u,b,q).$0()}else if((g&2)!==0)new P.aY(h,u,b).$0()
if(l!=null)$.d=l
g=u.b
if(!!J.q(g).$in){if(g.a>=4){k=H.h(o.c,"$it")
o.c=null
b=o.m(k)
o.a=g.a
o.c=g.c
h.a=g
continue}else P.aS(g,o)
return}}j=b.b
k=H.h(j.c,"$it")
j.c=null
b=j.m(k)
g=u.a
p=u.b
if(!g){H.p(p,H.m(j,0))
j.a=4
j.c=p}else{H.h(p,"$il")
j.a=8
j.c=p}h.a=j
g=j}},
cD:function(a,b){if(H.aa(a,{func:1,args:[P.e,P.k]}))return b.K(a,null,P.e,P.k)
if(H.aa(a,{func:1,args:[P.e]}))return H.c(a,{func:1,ret:null,args:[P.e]})
throw H.b(P.bG(a,"onError","Error handler must accept one Object or one Object and a StackTrace as arguments, and return a a valid result"))},
cC:function(){var u,t
for(;u=$.F,u!=null;){$.T=null
t=u.b
$.F=t
if(t==null)$.S=null
u.a.$0()}},
cH:function(){$.bu=!0
try{P.cC()}finally{$.T=null
$.bu=!1
if($.F!=null)$.bE().$1(P.bW())}},
bT:function(a){var u=new P.a8(a)
if($.F==null){$.F=$.S=u
if(!$.bu)$.bE().$1(P.bW())}else $.S=$.S.b=u},
cG:function(a){var u,t,s=$.F
if(s==null){P.bT(a)
$.T=$.S
return}u=new P.a8(a)
t=$.T
if(t==null){u.b=s
$.F=$.T=u}else{u.b=t.b
$.T=t.b=u
if(u.b==null)$.S=u}},
d4:function(a){var u=null,t=$.d
if(C.a===t){P.G(u,u,C.a,a)
return}P.G(u,u,t,H.c(t.J(a),{func:1,ret:-1}))},
db:function(a,b){H.ad(new P.w(!1,null,"stream","Must not be null"))
return new P.b4([b])},
bw:function(a,b,c,d,e){var u={}
u.a=d
P.cG(new P.ba(u,e))},
bS:function(a,b,c,d,e){var u,t=$.d
if(t===c)return d.$0()
$.d=c
u=t
try{t=d.$0()
return t}finally{$.d=u}},
cF:function(a,b,c,d,e,f,g){var u,t=$.d
if(t===c)return d.$1(e)
$.d=c
u=t
try{t=d.$1(e)
return t}finally{$.d=u}},
cE:function(a,b,c,d,e,f,g,h,i){var u,t=$.d
if(t===c)return d.$2(e,f)
$.d=c
u=t
try{t=d.$2(e,f)
return t}finally{$.d=u}},
G:function(a,b,c,d){var u
H.c(d,{func:1,ret:-1})
u=C.a!==c
if(u)d=!(!u||!1)?c.J(d):c.T(d,-1)
P.bT(d)},
aK:function aK(a){this.a=a},
aJ:function aJ(a,b,c){this.a=a
this.b=b
this.c=c},
aL:function aL(a){this.a=a},
aM:function aM(a){this.a=a},
b5:function b5(){},
b6:function b6(a,b){this.a=a
this.b=b},
aH:function aH(a,b){this.a=a
this.b=!1
this.$ti=b},
b8:function b8(a){this.a=a},
b9:function b9(a){this.a=a},
bb:function bb(a){this.a=a},
aN:function aN(){},
aI:function aI(a,b){this.a=a
this.$ti=b},
t:function t(a,b,c,d,e){var _=this
_.a=null
_.b=a
_.c=b
_.d=c
_.e=d
_.$ti=e},
j:function j(a,b){var _=this
_.a=0
_.b=a
_.c=null
_.$ti=b},
aP:function aP(a,b){this.a=a
this.b=b},
aX:function aX(a,b){this.a=a
this.b=b},
aT:function aT(a){this.a=a},
aU:function aU(a){this.a=a},
aV:function aV(a,b,c){this.a=a
this.b=b
this.c=c},
aR:function aR(a,b){this.a=a
this.b=b},
aW:function aW(a,b){this.a=a
this.b=b},
aQ:function aQ(a,b,c){this.a=a
this.b=b
this.c=c},
b_:function b_(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.d=d},
b0:function b0(a){this.a=a},
aZ:function aZ(a,b,c){this.a=a
this.b=b
this.c=c},
aY:function aY(a,b,c){this.a=a
this.b=b
this.c=c},
a8:function a8(a){this.a=a
this.b=null},
b4:function b4(a){this.$ti=a},
l:function l(a,b){this.a=a
this.b=b},
b7:function b7(){},
ba:function ba(a,b){this.a=a
this.b=b},
b1:function b1(){},
b3:function b3(a,b,c){this.a=a
this.b=b
this.c=c},
b2:function b2(a,b){this.a=a
this.b=b},
ck:function(a){if(a instanceof H.N)return a.h(0)
return"Instance of '"+H.a(H.a4(a))+"'"},
co:function(a,b,c){var u=new J.af(b,b.length,[H.m(b,0)])
if(!u.w())return a
if(c.length===0){do a+=H.a(u.d)
while(u.w())}else{a+=H.a(u.d)
for(;u.w();)a=a+c+H.a(u.d)}return a},
al:function(a){if(typeof a==="number"||typeof a==="boolean"||null==a)return J.ae(a)
if(typeof a==="string")return JSON.stringify(a)
return P.ck(a)},
bG:function(a,b,c){return new P.w(!0,a,b,c)},
bs:function(a,b){return new P.av(!0,a,b,"Value not in range")},
bP:function(a){return new P.aF(a)},
bO:function(a){return new P.aD(a)},
bM:function(a){return new P.ax(a)},
I:function I(){},
bd:function bd(){},
C:function C(){},
ag:function ag(){},
Q:function Q(){},
w:function w(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.d=d},
av:function av(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.d=d},
am:function am(a,b,c,d,e){var _=this
_.f=a
_.a=b
_.b=c
_.c=d
_.d=e},
aF:function aF(a){this.a=a},
aD:function aD(a){this.a=a},
ax:function ax(a){this.a=a},
ai:function ai(a){this.a=a},
a6:function a6(){},
aj:function aj(a){this.a=a},
aO:function aO(a){this.a=a},
A:function A(){},
as:function as(){},
f:function f(){},
Z:function Z(){},
e:function e(){},
k:function k(){},
r:function r(){},
a7:function a7(a){this.a=a},
d1:function(a,b){var u=new P.j($.d,[b]),t=new P.aI(u,[b])
a.then(H.W(new P.bj(t,b),1),H.W(new P.bk(t),1))
return u},
bj:function bj(a,b){this.a=a
this.b=b},
bk:function bk(a){this.a=a},
cm:function(a,b,c){var u,t
if(P.cA(a))return b+"..."+c
u=new P.a7(b)
C.e.I($.U,a)
try{t=u
t.a=P.co(t.a,a,", ")}finally{if(0>=$.U.length)return H.bA($.U,-1)
$.U.pop()}u.a+=c
t=u.a
return t.charCodeAt(0)==0?t:t},
cA:function(a){var u,t
for(u=$.U.length,t=0;t<u;++t)if(a===$.U[t])return!0
return!1}},W={ak:function ak(){},x:function x(){},a5:function a5(){}},M={
ab:function(){var u=0,t=P.cB(null),s
var $async$ab=P.cJ(function(a,b){if(a===1)return P.cv(b,t)
while(true)switch(u){case 0:s=window.navigator.serviceWorker
u=2
return P.cu(P.d1(s.register("/sw.js",null),W.a5),$async$ab)
case 2:return P.cw(null,t)}})
return P.cx($async$ab,t)}}
var w=[C,H,J,P,W,M]
hunkHelpers.setFunctionNamesIfNecessary(w)
var $={}
H.bq.prototype={}
J.i.prototype={
h:function(a){return"Instance of '"+H.a(H.a4(a))+"'"}}
J.an.prototype={
h:function(a){return String(a)},
$iI:1}
J.ap.prototype={
h:function(a){return"null"},
$if:1}
J.a3.prototype={
h:function(a){return String(a)}}
J.au.prototype={}
J.R.prototype={}
J.a2.prototype={
h:function(a){var u=a[$.c4()]
if(u==null)return this.M(a)
return"JavaScript function for "+H.a(J.ae(u))},
$S:function(){return{func:1,opt:[,,,,,,,,,,,,,,,,]}},
$ibo:1}
J.D.prototype={
I:function(a,b){H.p(b,H.m(a,0))
if(!!a.fixed$length)H.ad(P.bP("add"))
a.push(b)},
h:function(a){return P.cm(a,"[","]")},
gn:function(a){return a.length},
$icl:1}
J.bp.prototype={}
J.af.prototype={
w:function(){var u,t=this,s=t.a,r=s.length
if(t.b!==r)throw H.b(H.d5(s))
u=t.c
if(u>=r){t.sF(null)
return!1}t.sF(s[u]);++t.c
return!0},
sF:function(a){this.d=H.p(a,H.m(this,0))}}
J.aq.prototype={
h:function(a){if(a===0&&1/a<0)return"-0.0"
else return""+a},
S:function(a,b){var u
if(a>0)u=this.R(a,b)
else{u=b>31?31:b
u=a>>u>>>0}return u},
R:function(a,b){return b>31?0:a>>>b},
$iZ:1}
J.a1.prototype={$iA:1}
J.ao.prototype={}
J.P.prototype={
P:function(a,b){if(b>=a.length)throw H.b(H.bX(a,b))
return a.charCodeAt(b)},
j:function(a,b){if(typeof b!=="string")throw H.b(P.bG(b,null,null))
return a+b},
h:function(a){return a},
gn:function(a){return a.length},
$ir:1}
H.aA.prototype={
i:function(a){var u,t,s=this,r=new RegExp(s.a).exec(a)
if(r==null)return
u=Object.create(null)
t=s.b
if(t!==-1)u.arguments=r[t+1]
t=s.c
if(t!==-1)u.argumentsExpr=r[t+1]
t=s.d
if(t!==-1)u.expr=r[t+1]
t=s.e
if(t!==-1)u.method=r[t+1]
t=s.f
if(t!==-1)u.receiver=r[t+1]
return u}}
H.at.prototype={
h:function(a){var u=this.b
if(u==null)return"NoSuchMethodError: "+H.a(this.a)
return"NoSuchMethodError: method not found: '"+u+"' on null"}}
H.ar.prototype={
h:function(a){var u,t=this,s="NoSuchMethodError: method not found: '",r=t.b
if(r==null)return"NoSuchMethodError: "+H.a(t.a)
u=t.c
if(u==null)return s+r+"' ("+H.a(t.a)+")"
return s+r+"' on '"+u+"' ("+H.a(t.a)+")"}}
H.aE.prototype={
h:function(a){var u=this.a
return u.length===0?"Error":"Error: "+u}}
H.O.prototype={}
H.bm.prototype={
$1:function(a){if(!!J.q(a).$iC)if(a.$thrownJsError==null)a.$thrownJsError=this.a
return a},
$S:4}
H.a9.prototype={
h:function(a){var u,t=this.b
if(t!=null)return t
t=this.a
u=t!==null&&typeof t==="object"?t.stack:null
return this.b=u==null?"":u},
$ik:1}
H.N.prototype={
h:function(a){var u=this.constructor,t=u==null?null:u.name
return"Closure '"+H.L(t==null?"unknown":t)+"'"},
$ibo:1,
ga_:function(){return this},
$C:"$1",
$R:1,
$D:null}
H.az.prototype={}
H.ay.prototype={
h:function(a){var u=this.$static_name
if(u==null)return"Closure of unknown static method"
return"Closure '"+H.L(u)+"'"}}
H.a0.prototype={
h:function(a){var u=this.c
if(u==null)u=this.a
return"Closure '"+H.a(this.d)+"' of "+("Instance of '"+H.a(H.a4(u))+"'")}}
H.aC.prototype={
h:function(a){return this.a}}
H.aw.prototype={
h:function(a){return"RuntimeError: "+this.a}}
H.aG.prototype={
h:function(a){return"Assertion failed: "+P.al(this.a)}}
H.be.prototype={
$1:function(a){return this.a(a)},
$S:4}
H.bf.prototype={
$2:function(a,b){return this.a(a,b)},
$S:6}
H.bg.prototype={
$1:function(a){return this.a(H.B(a))},
$S:7}
P.aK.prototype={
$1:function(a){var u=this.a,t=u.a
u.a=null
t.$0()},
$S:5}
P.aJ.prototype={
$1:function(a){var u,t
this.a.a=H.c(a,{func:1,ret:-1})
u=this.b
t=this.c
u.firstChild?u.removeChild(t):u.appendChild(t)},
$S:8}
P.aL.prototype={
$0:function(){this.a.$0()},
$S:0}
P.aM.prototype={
$0:function(){this.a.$0()},
$S:0}
P.b5.prototype={
N:function(a,b){if(self.setTimeout!=null)self.setTimeout(H.W(new P.b6(this,b),0),a)
else throw H.b(P.bP("`setTimeout()` not found."))}}
P.b6.prototype={
$0:function(){this.b.$0()},
$S:1}
P.aH.prototype={
u:function(a){var u,t,s=this,r=H.m(s,0)
H.J(a,{futureOr:1,type:r})
u=!s.b||H.V(a,"$in",s.$ti,"$an")
t=s.a
if(u)t.C(a)
else t.E(H.p(a,r))},
v:function(a,b){var u=this.a
if(this.b)u.k(a,b)
else u.D(a,b)}}
P.b8.prototype={
$1:function(a){return this.a.$2(0,a)},
$S:2}
P.b9.prototype={
$2:function(a,b){this.a.$2(1,new H.O(a,H.h(b,"$ik")))},
$S:9}
P.bb.prototype={
$2:function(a,b){this.a(H.K(a),b)},
$S:10}
P.aN.prototype={
v:function(a,b){var u
if(a==null)a=new P.Q()
u=this.a
if(u.a!==0)throw H.b(P.bM("Future already completed"))
u.D(a,b)},
U:function(a){return this.v(a,null)}}
P.aI.prototype={
u:function(a){var u
H.J(a,{futureOr:1,type:H.m(this,0)})
u=this.a
if(u.a!==0)throw H.b(P.bM("Future already completed"))
u.C(a)}}
P.t.prototype={
W:function(a){if((this.c&15)!==6)return!0
return this.b.b.A(H.c(this.d,{func:1,ret:P.I,args:[P.e]}),a.a,P.I,P.e)},
V:function(a){var u=this.e,t=P.e,s={futureOr:1,type:H.m(this,1)},r=this.b.b
if(H.aa(u,{func:1,args:[P.e,P.k]}))return H.J(r.X(u,a.a,a.b,null,t,P.k),s)
else return H.J(r.A(H.c(u,{func:1,args:[P.e]}),a.a,null,t),s)}}
P.j.prototype={
B:function(a,b,c){var u,t,s,r=H.m(this,0)
H.c(a,{func:1,ret:{futureOr:1,type:c},args:[r]})
u=$.d
if(u!==C.a){H.c(a,{func:1,ret:{futureOr:1,type:c},args:[r]})
if(b!=null)b=P.cD(b,u)}t=new P.j($.d,[c])
s=b==null?1:3
this.p(new P.t(t,s,a,b,[r,c]))
return t},
Z:function(a,b){return this.B(a,null,b)},
H:function(a,b,c){var u,t=H.m(this,0)
H.c(a,{func:1,ret:{futureOr:1,type:c},args:[t]})
u=new P.j($.d,[c])
this.p(new P.t(u,(b==null?1:3)|16,a,b,[t,c]))
return u},
p:function(a){var u,t=this,s=t.a
if(s<=1){a.a=H.h(t.c,"$it")
t.c=a}else{if(s===2){u=H.h(t.c,"$ij")
s=u.a
if(s<4){u.p(a)
return}t.a=s
t.c=u.c}P.G(null,null,t.b,H.c(new P.aP(t,a),{func:1,ret:-1}))}},
G:function(a){var u,t,s,r,q,p=this,o={}
o.a=a
if(a==null)return
u=p.a
if(u<=1){t=H.h(p.c,"$it")
s=p.c=a
if(t!=null){for(;r=s.a,r!=null;s=r);s.a=t}}else{if(u===2){q=H.h(p.c,"$ij")
u=q.a
if(u<4){q.G(a)
return}p.a=u
p.c=q.c}o.a=p.m(a)
P.G(null,null,p.b,H.c(new P.aX(o,p),{func:1,ret:-1}))}},
l:function(){var u=H.h(this.c,"$it")
this.c=null
return this.m(u)},
m:function(a){var u,t,s
for(u=a,t=null;u!=null;t=u,u=s){s=u.a
u.a=t}return t},
E:function(a){var u,t=this
H.p(a,H.m(t,0))
u=t.l()
t.a=4
t.c=a
P.E(t,u)},
k:function(a,b){var u,t=this
H.h(b,"$ik")
u=t.l()
t.a=8
t.c=new P.l(a,b)
P.E(t,u)},
C:function(a){var u=this
H.J(a,{futureOr:1,type:H.m(u,0)})
if(H.V(a,"$in",u.$ti,"$an")){u.O(a)
return}u.a=1
P.G(null,null,u.b,H.c(new P.aR(u,a),{func:1,ret:-1}))},
O:function(a){var u=this,t=u.$ti
H.cL(a,"$in",t,"$an")
if(H.V(a,"$ij",t,null)){if(a.a===8){u.a=1
P.G(null,null,u.b,H.c(new P.aW(u,a),{func:1,ret:-1}))}else P.aS(a,u)
return}P.bQ(a,u)},
D:function(a,b){this.a=1
P.G(null,null,this.b,H.c(new P.aQ(this,a,b),{func:1,ret:-1}))},
$in:1}
P.aP.prototype={
$0:function(){P.E(this.a,this.b)},
$S:0}
P.aX.prototype={
$0:function(){P.E(this.b,this.a.a)},
$S:0}
P.aT.prototype={
$1:function(a){var u,t,s=this.a
s.a=0
u=H.m(s,0)
H.J(a,{futureOr:1,type:u})
if(H.V(a,"$in",[u],"$an"))if(H.V(a,"$ij",[u],null))P.aS(a,s)
else P.bQ(a,s)
else{t=s.l()
H.p(a,u)
s.a=4
s.c=a
P.E(s,t)}},
$S:5}
P.aU.prototype={
$2:function(a,b){H.h(b,"$ik")
this.a.k(a,b)},
$1:function(a){return this.$2(a,null)},
$S:11}
P.aV.prototype={
$0:function(){this.a.k(this.b,this.c)},
$S:0}
P.aR.prototype={
$0:function(){var u=this.a
u.E(H.p(this.b,H.m(u,0)))},
$S:0}
P.aW.prototype={
$0:function(){P.aS(this.b,this.a)},
$S:0}
P.aQ.prototype={
$0:function(){this.a.k(this.b,this.c)},
$S:0}
P.b_.prototype={
$0:function(){var u,t,s,r,q,p,o=this,n=null
try{s=o.c
n=s.b.b.L(H.c(s.d,{func:1}),null)}catch(r){u=H.a_(r)
t=H.Y(r)
if(o.d){s=H.h(o.a.a.c,"$il").a
q=u
q=s==null?q==null:s===q
s=q}else s=!1
q=o.b
if(s)q.b=H.h(o.a.a.c,"$il")
else q.b=new P.l(u,t)
q.a=!0
return}if(!!J.q(n).$in){if(n instanceof P.j&&n.a>=4){if(n.a===8){s=o.b
s.b=H.h(n.c,"$il")
s.a=!0}return}p=o.a.a
s=o.b
s.b=n.Z(new P.b0(p),null)
s.a=!1}},
$S:1}
P.b0.prototype={
$1:function(a){return this.a},
$S:12}
P.aZ.prototype={
$0:function(){var u,t,s,r,q,p,o,n=this
try{s=n.b
r=H.m(s,0)
q=H.p(n.c,r)
p=H.m(s,1)
n.a.b=s.b.b.A(H.c(s.d,{func:1,ret:{futureOr:1,type:p},args:[r]}),q,{futureOr:1,type:p},r)}catch(o){u=H.a_(o)
t=H.Y(o)
s=n.a
s.b=new P.l(u,t)
s.a=!0}},
$S:1}
P.aY.prototype={
$0:function(){var u,t,s,r,q,p,o,n,m=this
try{u=H.h(m.a.a.c,"$il")
r=m.c
if(H.cQ(r.W(u))&&r.e!=null){q=m.b
q.b=r.V(u)
q.a=!1}}catch(p){t=H.a_(p)
s=H.Y(p)
r=H.h(m.a.a.c,"$il")
q=r.a
o=t
n=m.b
if(q==null?o==null:q===o)n.b=r
else n.b=new P.l(t,s)
n.a=!0}},
$S:1}
P.a8.prototype={}
P.b4.prototype={}
P.l.prototype={
h:function(a){return H.a(this.a)},
$iC:1}
P.b7.prototype={$idm:1}
P.ba.prototype={
$0:function(){var u,t=this.a,s=t.a
t=s==null?t.a=new P.Q():s
s=this.b
if(s==null)throw H.b(t)
u=H.b(t)
u.stack=s.h(0)
throw u},
$S:0}
P.b1.prototype={
Y:function(a){var u,t,s,r=null
H.c(a,{func:1,ret:-1})
try{if(C.a===$.d){a.$0()
return}P.bS(r,r,this,a,-1)}catch(s){u=H.a_(s)
t=H.Y(s)
P.bw(r,r,this,u,H.h(t,"$ik"))}},
T:function(a,b){return new P.b3(this,H.c(a,{func:1,ret:b}),b)},
J:function(a){return new P.b2(this,H.c(a,{func:1,ret:-1}))},
L:function(a,b){H.c(a,{func:1,ret:b})
if($.d===C.a)return a.$0()
return P.bS(null,null,this,a,b)},
A:function(a,b,c,d){H.c(a,{func:1,ret:c,args:[d]})
H.p(b,d)
if($.d===C.a)return a.$1(b)
return P.cF(null,null,this,a,b,c,d)},
X:function(a,b,c,d,e,f){H.c(a,{func:1,ret:d,args:[e,f]})
H.p(b,e)
H.p(c,f)
if($.d===C.a)return a.$2(b,c)
return P.cE(null,null,this,a,b,c,d,e,f)},
K:function(a,b,c,d){return H.c(a,{func:1,ret:b,args:[c,d]})}}
P.b3.prototype={
$0:function(){return this.a.L(this.b,this.c)},
$S:function(){return{func:1,ret:this.c}}}
P.b2.prototype={
$0:function(){return this.a.Y(this.b)},
$S:1}
P.I.prototype={}
P.bd.prototype={}
P.C.prototype={}
P.ag.prototype={
h:function(a){return"Assertion failed"}}
P.Q.prototype={
h:function(a){return"Throw of null."}}
P.w.prototype={
gt:function(){return"Invalid argument"+(!this.a?"(s)":"")},
gq:function(){return""},
h:function(a){var u,t,s,r,q=this,p=q.c,o=p!=null?" ("+p+")":""
p=q.d
u=p==null?"":": "+p
t=q.gt()+o+u
if(!q.a)return t
s=q.gq()
r=P.al(q.b)
return t+s+": "+r}}
P.av.prototype={
gt:function(){return"RangeError"},
gq:function(){return""}}
P.am.prototype={
gt:function(){return"RangeError"},
gq:function(){var u,t=H.K(this.b)
if(typeof t!=="number")return t.a0()
if(t<0)return": index must not be negative"
u=this.f
if(u===0)return": no indices are valid"
return": index should be less than "+u},
gn:function(a){return this.f}}
P.aF.prototype={
h:function(a){return"Unsupported operation: "+this.a}}
P.aD.prototype={
h:function(a){var u=this.a
return u!=null?"UnimplementedError: "+u:"UnimplementedError"}}
P.ax.prototype={
h:function(a){return"Bad state: "+this.a}}
P.ai.prototype={
h:function(a){var u=this.a
if(u==null)return"Concurrent modification during iteration."
return"Concurrent modification during iteration: "+P.al(u)+"."}}
P.a6.prototype={
h:function(a){return"Stack Overflow"},
$iC:1}
P.aj.prototype={
h:function(a){var u=this.a
return u==null?"Reading static variable during its initialization":"Reading static variable '"+u+"' during its initialization"}}
P.aO.prototype={
h:function(a){return"Exception: "+this.a}}
P.A.prototype={}
P.as.prototype={$icl:1}
P.f.prototype={
h:function(a){return"null"}}
P.Z.prototype={}
P.e.prototype={constructor:P.e,$ie:1,
h:function(a){return"Instance of '"+H.a(H.a4(this))+"'"},
toString:function(){return this.h(this)}}
P.k.prototype={}
P.r.prototype={}
P.a7.prototype={
gn:function(a){return this.a.length},
h:function(a){var u=this.a
return u.charCodeAt(0)==0?u:u}}
W.ak.prototype={
h:function(a){return String(a)}}
W.x.prototype={}
W.a5.prototype={$ia5:1}
P.bj.prototype={
$1:function(a){return this.a.u(H.J(a,{futureOr:1,type:this.b}))},
$S:2}
P.bk.prototype={
$1:function(a){return this.a.U(a)},
$S:2};(function aliases(){var u=J.a3.prototype
u.M=u.h})();(function installTearOffs(){var u=hunkHelpers._static_1,t=hunkHelpers._static_0
u(P,"cN","cq",3)
u(P,"cO","cr",3)
u(P,"cP","cs",3)
t(P,"bW","cH",1)})();(function inheritance(){var u=hunkHelpers.inherit,t=hunkHelpers.inheritMany
u(P.e,null)
t(P.e,[H.bq,J.i,J.af,H.aA,P.C,H.O,H.N,H.a9,P.b5,P.aH,P.aN,P.t,P.j,P.a8,P.b4,P.l,P.b7,P.I,P.Z,P.a6,P.aO,P.as,P.f,P.k,P.r,P.a7])
t(J.i,[J.an,J.ap,J.a3,J.D,J.aq,J.P,W.ak,W.x])
t(J.a3,[J.au,J.R,J.a2])
u(J.bp,J.D)
t(J.aq,[J.a1,J.ao])
t(P.C,[H.at,H.ar,H.aE,H.aC,H.aw,P.ag,P.Q,P.w,P.aF,P.aD,P.ax,P.ai,P.aj])
t(H.N,[H.bm,H.az,H.be,H.bf,H.bg,P.aK,P.aJ,P.aL,P.aM,P.b6,P.b8,P.b9,P.bb,P.aP,P.aX,P.aT,P.aU,P.aV,P.aR,P.aW,P.aQ,P.b_,P.b0,P.aZ,P.aY,P.ba,P.b3,P.b2,P.bj,P.bk])
t(H.az,[H.ay,H.a0])
u(H.aG,P.ag)
u(P.aI,P.aN)
u(P.b1,P.b7)
t(P.Z,[P.bd,P.A])
t(P.w,[P.av,P.am])
u(W.a5,W.x)})()
var v={mangledGlobalNames:{A:"int",bd:"double",Z:"num",r:"String",I:"bool",f:"Null",as:"List"},mangledNames:{},getTypeFromName:getGlobalFromName,metadata:[],types:[{func:1,ret:P.f},{func:1,ret:-1},{func:1,ret:-1,args:[,]},{func:1,ret:-1,args:[{func:1,ret:-1}]},{func:1,args:[,]},{func:1,ret:P.f,args:[,]},{func:1,args:[,P.r]},{func:1,args:[P.r]},{func:1,ret:P.f,args:[{func:1,ret:-1}]},{func:1,ret:P.f,args:[,P.k]},{func:1,ret:P.f,args:[P.A,,]},{func:1,ret:P.f,args:[,],opt:[P.k]},{func:1,ret:[P.j,,],args:[,]}],interceptorsByTag:null,leafTags:null};(function constants(){C.o=J.i.prototype
C.e=J.D.prototype
C.p=J.a1.prototype
C.f=J.P.prototype
C.q=J.a2.prototype
C.h=J.au.prototype
C.b=J.R.prototype
C.c=function getTagFallback(o) {
  var s = Object.prototype.toString.call(o);
  return s.substring(8, s.length - 1);
}
C.i=function() {
  var toStringFunction = Object.prototype.toString;
  function getTag(o) {
    var s = toStringFunction.call(o);
    return s.substring(8, s.length - 1);
  }
  function getUnknownTag(object, tag) {
    if (/^HTML[A-Z].*Element$/.test(tag)) {
      var name = toStringFunction.call(object);
      if (name == "[object Object]") return null;
      return "HTMLElement";
    }
  }
  function getUnknownTagGenericBrowser(object, tag) {
    if (self.HTMLElement && object instanceof HTMLElement) return "HTMLElement";
    return getUnknownTag(object, tag);
  }
  function prototypeForTag(tag) {
    if (typeof window == "undefined") return null;
    if (typeof window[tag] == "undefined") return null;
    var constructor = window[tag];
    if (typeof constructor != "function") return null;
    return constructor.prototype;
  }
  function discriminator(tag) { return null; }
  var isBrowser = typeof navigator == "object";
  return {
    getTag: getTag,
    getUnknownTag: isBrowser ? getUnknownTagGenericBrowser : getUnknownTag,
    prototypeForTag: prototypeForTag,
    discriminator: discriminator };
}
C.n=function(getTagFallback) {
  return function(hooks) {
    if (typeof navigator != "object") return hooks;
    var ua = navigator.userAgent;
    if (ua.indexOf("DumpRenderTree") >= 0) return hooks;
    if (ua.indexOf("Chrome") >= 0) {
      function confirm(p) {
        return typeof window == "object" && window[p] && window[p].name == p;
      }
      if (confirm("Window") && confirm("HTMLElement")) return hooks;
    }
    hooks.getTag = getTagFallback;
  };
}
C.j=function(hooks) {
  if (typeof dartExperimentalFixupGetTag != "function") return hooks;
  hooks.getTag = dartExperimentalFixupGetTag(hooks.getTag);
}
C.k=function(hooks) {
  var getTag = hooks.getTag;
  var prototypeForTag = hooks.prototypeForTag;
  function getTagFixed(o) {
    var tag = getTag(o);
    if (tag == "Document") {
      if (!!o.xmlVersion) return "!Document";
      return "!HTMLDocument";
    }
    return tag;
  }
  function prototypeForTagFixed(tag) {
    if (tag == "Document") return null;
    return prototypeForTag(tag);
  }
  hooks.getTag = getTagFixed;
  hooks.prototypeForTag = prototypeForTagFixed;
}
C.m=function(hooks) {
  var userAgent = typeof navigator == "object" ? navigator.userAgent : "";
  if (userAgent.indexOf("Firefox") == -1) return hooks;
  var getTag = hooks.getTag;
  var quickMap = {
    "BeforeUnloadEvent": "Event",
    "DataTransfer": "Clipboard",
    "GeoGeolocation": "Geolocation",
    "Location": "!Location",
    "WorkerMessageEvent": "MessageEvent",
    "XMLDocument": "!Document"};
  function getTagFirefox(o) {
    var tag = getTag(o);
    return quickMap[tag] || tag;
  }
  hooks.getTag = getTagFirefox;
}
C.l=function(hooks) {
  var userAgent = typeof navigator == "object" ? navigator.userAgent : "";
  if (userAgent.indexOf("Trident/") == -1) return hooks;
  var getTag = hooks.getTag;
  var quickMap = {
    "BeforeUnloadEvent": "Event",
    "DataTransfer": "Clipboard",
    "HTMLDDElement": "HTMLElement",
    "HTMLDTElement": "HTMLElement",
    "HTMLPhraseElement": "HTMLElement",
    "Position": "Geoposition"
  };
  function getTagIE(o) {
    var tag = getTag(o);
    var newTag = quickMap[tag];
    if (newTag) return newTag;
    if (tag == "Object") {
      if (window.DataView && (o instanceof window.DataView)) return "DataView";
    }
    return tag;
  }
  function prototypeForTagIE(tag) {
    var constructor = window[tag];
    if (constructor == null) return null;
    return constructor.prototype;
  }
  hooks.getTag = getTagIE;
  hooks.prototypeForTag = prototypeForTagIE;
}
C.d=function(hooks) { return hooks; }

C.a=new P.b1()})();(function staticFields(){$.u=0
$.M=null
$.bH=null
$.bt=!1
$.c_=null
$.bU=null
$.c2=null
$.bc=null
$.bh=null
$.bz=null
$.F=null
$.S=null
$.T=null
$.bu=!1
$.d=C.a
$.U=[]})();(function lazyInitializers(){var u=hunkHelpers.lazy
u($,"d8","c4",function(){return H.bZ("_$dart_dartClosure")})
u($,"d9","bD",function(){return H.bZ("_$dart_js")})
u($,"dc","c5",function(){return H.v(H.aB({
toString:function(){return"$receiver$"}}))})
u($,"dd","c6",function(){return H.v(H.aB({$method$:null,
toString:function(){return"$receiver$"}}))})
u($,"de","c7",function(){return H.v(H.aB(null))})
u($,"df","c8",function(){return H.v(function(){var $argumentsExpr$='$arguments$'
try{null.$method$($argumentsExpr$)}catch(t){return t.message}}())})
u($,"di","cb",function(){return H.v(H.aB(void 0))})
u($,"dj","cc",function(){return H.v(function(){var $argumentsExpr$='$arguments$'
try{(void 0).$method$($argumentsExpr$)}catch(t){return t.message}}())})
u($,"dh","ca",function(){return H.v(H.bN(null))})
u($,"dg","c9",function(){return H.v(function(){try{null.$method$}catch(t){return t.message}}())})
u($,"dl","ce",function(){return H.v(H.bN(void 0))})
u($,"dk","cd",function(){return H.v(function(){try{(void 0).$method$}catch(t){return t.message}}())})
u($,"dn","bE",function(){return P.cp()})})();(function nativeSupport(){!function(){var u=function(a){var o={}
o[a]=1
return Object.keys(hunkHelpers.convertToFastObject(o))[0]}
v.getIsolateTag=function(a){return u("___dart_"+a+v.isolateTag)}
var t="___dart_isolate_tags_"
var s=Object[t]||(Object[t]=Object.create(null))
var r="_ZxYxX"
for(var q=0;;q++){var p=u(r+"_"+q+"_")
if(!(p in s)){s[p]=1
v.isolateTag=p
break}}v.dispatchPropertyName=v.getIsolateTag("dispatch_record")}()
hunkHelpers.setOrUpdateInterceptorsByTag({ApplicationCacheErrorEvent:J.i,DOMError:J.i,ErrorEvent:J.i,Event:J.i,InputEvent:J.i,MediaError:J.i,Navigator:J.i,NavigatorConcurrentHardware:J.i,NavigatorUserMediaError:J.i,OverconstrainedError:J.i,PositionError:J.i,SensorErrorEvent:J.i,SpeechRecognitionError:J.i,SQLError:J.i,DOMException:W.ak,EventTarget:W.x,ServiceWorkerContainer:W.x,Window:W.x,DOMWindow:W.x})
hunkHelpers.setOrUpdateLeafTags({ApplicationCacheErrorEvent:true,DOMError:true,ErrorEvent:true,Event:true,InputEvent:true,MediaError:true,Navigator:true,NavigatorConcurrentHardware:true,NavigatorUserMediaError:true,OverconstrainedError:true,PositionError:true,SensorErrorEvent:true,SpeechRecognitionError:true,SQLError:true,DOMException:true,EventTarget:true,ServiceWorkerContainer:true,Window:true,DOMWindow:true})})()
convertAllToFastObject(w)
convertToFastObject($);(function(a){if(typeof document==="undefined"){a(null)
return}if(typeof document.currentScript!='undefined'){a(document.currentScript)
return}var u=document.scripts
function onLoad(b){for(var s=0;s<u.length;++s)u[s].removeEventListener("load",onLoad,false)
a(b.target)}for(var t=0;t<u.length;++t)u[t].addEventListener("load",onLoad,false)})(function(a){v.currentScript=a
if(typeof dartMainRunner==="function")dartMainRunner(M.ab,[])
else M.ab([])})})()
//# sourceMappingURL=devices.dart.js.map
