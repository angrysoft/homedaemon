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
a[c]=function(){a[c]=function(){H.d8(b)}
var t
var s=d
try{if(a[b]===u){t=a[b]=s
t=a[b]=d()}else t=a[b]}finally{if(t===s)a[b]=null
a[c]=function(){return this[b]}}return t}}function makeConstList(a){a.immutable$list=Array
a.fixed$length=Array
return a}function convertToFastObject(a){function t(){}t.prototype=a
new t()
return a}function convertAllToFastObject(a){for(var u=0;u<a.length;++u)convertToFastObject(a[u])}var y=0
function tearOffGetter(a,b,c,d,e){return e?new Function("funcs","applyTrampolineIndex","reflectionInfo","name","H","c","return function tearOff_"+d+y+++"(receiver) {"+"if (c === null) c = "+"H.bz"+"("+"this, funcs, applyTrampolineIndex, reflectionInfo, false, true, name);"+"return new c(this, funcs[0], receiver, name);"+"}")(a,b,c,d,H,null):new Function("funcs","applyTrampolineIndex","reflectionInfo","name","H","c","return function tearOff_"+d+y+++"() {"+"if (c === null) c = "+"H.bz"+"("+"this, funcs, applyTrampolineIndex, reflectionInfo, false, false, name);"+"return new c(this, funcs[0], null, name);"+"}")(a,b,c,d,H,null)}function tearOff(a,b,c,d,e,f){var u=null
return d?function(){if(u===null)u=H.bz(this,a,b,c,true,false,e).prototype
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
if(w[u][a])return w[u][a]}}var C={},H={br:function br(){},
M:function(a){var u,t=H.d9(a)
if(typeof t==="string")return t
u="minified:"+a
return u},
cV:function(a){return v.types[H.L(a)]},
a:function(a){var u
if(typeof a==="string")return a
if(typeof a==="number"){if(a!==0)return""+a}else if(!0===a)return"true"
else if(!1===a)return"false"
else if(a==null)return"null"
u=J.ae(a)
if(typeof u!=="string")throw H.b(H.cL(a))
return u},
a5:function(a){return H.co(a)+H.bw(H.Y(a),0,null)},
co:function(a){var u,t,s,r,q,p,o,n,m=null,l=J.q(a),k=l.constructor
if(typeof k=="function"){u=k.name
t=typeof u==="string"?u:m}else t=m
s=t==null
if(s||l===C.o||!!l.$iS){r=C.c(a)
if(s)t=r
if(r==="Object"){q=a.constructor
if(typeof q=="function"){p=String(q).match(/^\s*function\s*([\w$]*)\s*\(/)
o=p==null?m:p[1]
if(typeof o==="string"&&/^\w+$/.test(o))t=o}}return t}t=t
n=t.length
if(n>1&&C.f.R(t,0)===36){if(1>n)H.ad(P.bt(1,m))
if(n>n)H.ad(P.bt(n,m))
t=t.substring(1,n)}return H.M(t)},
bB:function(a,b){if(a==null)J.bG(a)
throw H.b(H.bY(a,b))},
bY:function(a,b){var u,t="index"
if(typeof b!=="number"||Math.floor(b)!==b)return new P.w(!0,b,t,null)
u=J.bG(a)
if(b<0||b>=u)return new P.am(u,!0,b,t,"Index out of range")
return P.bt(b,t)},
cL:function(a){return new P.w(!0,a,null,null)},
b:function(a){var u
if(a==null)a=new P.R()
u=new Error()
u.dartException=a
if("defineProperty" in Object){Object.defineProperty(u,"message",{get:H.c4})
u.name=""}else u.toString=H.c4
return u},
c4:function(){return J.ae(this.dartException)},
ad:function(a){throw H.b(a)},
d7:function(a){throw H.b(new P.ai(a))},
v:function(a){var u,t,s,r,q,p
a=H.d5(a.replace(String({}),'$receiver$'))
u=a.match(/\\\$[a-zA-Z]+\\\$/g)
if(u==null)u=H.bD([],[P.r])
t=u.indexOf("\\$arguments\\$")
s=u.indexOf("\\$argumentsExpr\\$")
r=u.indexOf("\\$expr\\$")
q=u.indexOf("\\$method\\$")
p=u.indexOf("\\$receiver\\$")
return new H.aA(a.replace(new RegExp('\\\\\\$arguments\\\\\\$','g'),'((?:x|[^x])*)').replace(new RegExp('\\\\\\$argumentsExpr\\\\\\$','g'),'((?:x|[^x])*)').replace(new RegExp('\\\\\\$expr\\\\\\$','g'),'((?:x|[^x])*)').replace(new RegExp('\\\\\\$method\\\\\\$','g'),'((?:x|[^x])*)').replace(new RegExp('\\\\\\$receiver\\\\\\$','g'),'((?:x|[^x])*)'),t,s,r,q,p)},
aB:function(a){return function($expr$){var $argumentsExpr$='$arguments$'
try{$expr$.$method$($argumentsExpr$)}catch(u){return u.message}}(a)},
bO:function(a){return function($expr$){try{$expr$.$method$}catch(u){return u.message}}(a)},
bM:function(a,b){return new H.at(a,b==null?null:b.method)},
bs:function(a,b){var u=b==null,t=u?null:b.method
return new H.ar(a,t,u?null:b.receiver)},
a0:function(a){var u,t,s,r,q,p,o,n,m,l,k,j,i,h,g=null,f=new H.bn(a)
if(a==null)return
if(a instanceof H.P)return f.$1(a.a)
if(typeof a!=="object")return a
if("dartException" in a)return f.$1(a.dartException)
else if(!("message" in a))return a
u=a.message
if("number" in a&&typeof a.number=="number"){t=a.number
s=t&65535
if((C.p.T(t,16)&8191)===10)switch(s){case 438:return f.$1(H.bs(H.a(u)+" (Error "+s+")",g))
case 445:case 5007:return f.$1(H.bM(H.a(u)+" (Error "+s+")",g))}}if(a instanceof TypeError){r=$.c6()
q=$.c7()
p=$.c8()
o=$.c9()
n=$.cc()
m=$.cd()
l=$.cb()
$.ca()
k=$.cf()
j=$.ce()
i=r.i(u)
if(i!=null)return f.$1(H.bs(H.C(u),i))
else{i=q.i(u)
if(i!=null){i.method="call"
return f.$1(H.bs(H.C(u),i))}else{i=p.i(u)
if(i==null){i=o.i(u)
if(i==null){i=n.i(u)
if(i==null){i=m.i(u)
if(i==null){i=l.i(u)
if(i==null){i=o.i(u)
if(i==null){i=k.i(u)
if(i==null){i=j.i(u)
h=i!=null}else h=!0}else h=!0}else h=!0}else h=!0}else h=!0}else h=!0}else h=!0
if(h)return f.$1(H.bM(H.C(u),i))}}return f.$1(new H.aE(typeof u==="string"?u:""))}if(a instanceof RangeError){if(typeof u==="string"&&u.indexOf("call stack")!==-1)return new P.a6()
u=function(b){try{return String(b)}catch(e){}return null}(a)
return f.$1(new P.w(!1,g,g,typeof u==="string"?u.replace(/^RangeError:\s*/,""):u))}if(typeof InternalError=="function"&&a instanceof InternalError)if(typeof u==="string"&&u==="too much recursion")return new P.a6()
return a},
Z:function(a){var u
if(a instanceof H.P)return a.b
if(a==null)return new H.a9(a)
u=a.$cachedTrace
if(u!=null)return u
return a.$cachedTrace=new H.a9(a)},
cZ:function(a,b,c,d,e,f){H.h(a,"$ibp")
switch(H.L(b)){case 0:return a.$0()
case 1:return a.$1(c)
case 2:return a.$2(c,d)
case 3:return a.$3(c,d,e)
case 4:return a.$4(c,d,e,f)}throw H.b(new P.aO("Unsupported number of arguments for wrapped closure"))},
X:function(a,b){var u=a.$identity
if(!!u)return u
u=function(c,d,e){return function(f,g,h,i){return e(c,d,f,g,h,i)}}(a,b,H.cZ)
a.$identity=u
return u},
ck:function(a,b,c,d,e,f,g){var u,t,s,r,q,p,o,n,m=null,l=b[0],k=l.$callName,j=e?Object.create(new H.ay().constructor.prototype):Object.create(new H.a1(m,m,m,m).constructor.prototype)
j.$initialize=j.constructor
if(e)u=function static_tear_off(){this.$initialize()}
else{t=$.u
if(typeof t!=="number")return t.j()
$.u=t+1
t=new Function("a,b,c,d"+t,"this.$initialize(a,b,c,d"+t+")")
u=t}j.constructor=u
u.prototype=j
if(!e){s=H.bK(a,l,f)
s.$reflectionInfo=d}else{j.$static_name=g
s=l}r=H.cg(d,e,f)
j.$S=r
j[k]=s
for(q=s,p=1;p<b.length;++p){o=b[p]
n=o.$callName
if(n!=null){o=e?o:H.bK(a,o,f)
j[n]=o}if(p===c){o.$reflectionInfo=d
q=o}}j.$C=q
j.$R=l.$R
j.$D=l.$D
return u},
cg:function(a,b,c){var u
if(typeof a=="number")return function(d,e){return function(){return d(e)}}(H.cV,a)
if(typeof a=="function")if(b)return a
else{u=c?H.bJ:H.bo
return function(d,e){return function(){return d.apply({$receiver:e(this)},arguments)}}(a,u)}throw H.b("Error in functionType of tearoff")},
ch:function(a,b,c,d){var u=H.bo
switch(b?-1:a){case 0:return function(e,f){return function(){return f(this)[e]()}}(c,u)
case 1:return function(e,f){return function(g){return f(this)[e](g)}}(c,u)
case 2:return function(e,f){return function(g,h){return f(this)[e](g,h)}}(c,u)
case 3:return function(e,f){return function(g,h,i){return f(this)[e](g,h,i)}}(c,u)
case 4:return function(e,f){return function(g,h,i,j){return f(this)[e](g,h,i,j)}}(c,u)
case 5:return function(e,f){return function(g,h,i,j,k){return f(this)[e](g,h,i,j,k)}}(c,u)
default:return function(e,f){return function(){return e.apply(f(this),arguments)}}(d,u)}},
bK:function(a,b,c){var u,t,s,r,q,p,o
if(c)return H.cj(a,b)
u=b.$stubName
t=b.length
s=a[u]
r=b==null?s==null:b===s
q=!r||t>=27
if(q)return H.ch(t,!r,u,b)
if(t===0){r=$.u
if(typeof r!=="number")return r.j()
$.u=r+1
p="self"+r
r="return function(){var "+p+" = this."
q=$.N
return new Function(r+H.a(q==null?$.N=H.ah("self"):q)+";return "+p+"."+H.a(u)+"();}")()}o="abcdefghijklmnopqrstuvwxyz".split("").splice(0,t).join(",")
r=$.u
if(typeof r!=="number")return r.j()
$.u=r+1
o+=r
r="return function("+o+"){return this."
q=$.N
return new Function(r+H.a(q==null?$.N=H.ah("self"):q)+"."+H.a(u)+"("+o+");}")()},
ci:function(a,b,c,d){var u=H.bo,t=H.bJ
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
cj:function(a,b){var u,t,s,r,q,p,o,n=$.N
if(n==null)n=$.N=H.ah("self")
u=$.bI
if(u==null)u=$.bI=H.ah("receiver")
t=b.$stubName
s=b.length
r=a[t]
q=b==null?r==null:b===r
p=!q||s>=28
if(p)return H.ci(s,!q,t,b)
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
bz:function(a,b,c,d,e,f,g){return H.ck(a,b,c,d,!!e,!!f,g)},
bo:function(a){return a.a},
bJ:function(a){return a.c},
ah:function(a){var u,t,s,r=new H.a1("self","target","receiver","name"),q=J.bL(Object.getOwnPropertyNames(r))
for(u=q.length,t=0;t<u;++t){s=q[t]
if(r[s]===a)return s}},
cR:function(a){if(a==null)H.cN("boolean expression must not be null")
return a},
C:function(a){if(a==null)return a
if(typeof a==="string")return a
throw H.b(H.z(a,"String"))},
dr:function(a){if(a==null)return a
if(typeof a==="boolean")return a
throw H.b(H.z(a,"bool"))},
L:function(a){if(a==null)return a
if(typeof a==="number"&&Math.floor(a)===a)return a
throw H.b(H.z(a,"int"))},
d4:function(a,b){throw H.b(H.z(a,H.M(H.C(b).substring(2))))},
h:function(a,b){if(a==null)return a
if((typeof a==="object"||typeof a==="function")&&J.q(a)[b])return a
H.d4(a,b)},
bZ:function(a){var u
if("$S" in a){u=a.$S
if(typeof u=="number")return v.types[H.L(u)]
else return a.$S()}return},
aa:function(a,b){var u
if(typeof a=="function")return!0
u=H.bZ(J.q(a))
if(u==null)return!1
return H.bS(u,null,b,null)},
c:function(a,b){var u,t
if(a==null)return a
if($.bu)return a
$.bu=!0
try{if(H.aa(a,b))return a
u=H.bm(b)
t=H.z(a,u)
throw H.b(t)}finally{$.bu=!1}},
K:function(a,b){if(a!=null&&!H.by(a,b))H.ad(H.z(a,H.bm(b)))
return a},
z:function(a,b){return new H.aC("TypeError: "+P.al(a)+": type '"+H.a(H.cJ(a))+"' is not a subtype of type '"+b+"'")},
cJ:function(a){var u,t=J.q(a)
if(!!t.$iO){u=H.bZ(t)
if(u!=null)return H.bm(u)
return"Closure"}return H.a5(a)},
cN:function(a){throw H.b(new H.aG(a))},
d8:function(a){throw H.b(new P.aj(a))},
c_:function(a){return v.getIsolateTag(a)},
bD:function(a,b){a.$ti=b
return a},
Y:function(a){if(a==null)return
return a.$ti},
du:function(a,b,c){return H.ac(a["$a"+H.a(c)],H.Y(b))},
m:function(a,b){var u=H.Y(a)
return u==null?null:u[b]},
bm:function(a){return H.A(a,null)},
A:function(a,b){var u,t
if(a==null)return"dynamic"
if(a===-1)return"void"
if(typeof a==="object"&&a!==null&&a.constructor===Array)return H.M(a[0].name)+H.bw(a,1,b)
if(typeof a=="function")return H.M(a.name)
if(a===-2)return"dynamic"
if(typeof a==="number"){H.L(a)
if(b==null||a<0||a>=b.length)return"unexpected-generic-index:"+a
u=b.length
t=u-a-1
if(t<0||t>=u)return H.bB(b,t)
return H.a(b[t])}if('func' in a)return H.cA(a,b)
if('futureOr' in a)return"FutureOr<"+H.A("type" in a?a.type:null,b)+">"
return"unknown-reified-type"},
cA:function(a,a0){var u,t,s,r,q,p,o,n,m,l,k,j,i,h,g,f,e,d,c,b=", "
if("bounds" in a){u=a.bounds
if(a0==null){a0=H.bD([],[P.r])
t=null}else t=a0.length
s=a0.length
for(r=u.length,q=r;q>0;--q)C.e.I(a0,"T"+(s+q))
for(p="<",o="",q=0;q<r;++q,o=b){p+=o
n=a0.length
m=n-q-1
if(m<0)return H.bB(a0,m)
p=C.f.j(p,a0[m])
l=u[q]
if(l!=null&&l!==P.f)p+=" extends "+H.A(l,a0)}p+=">"}else{p=""
t=null}k=!!a.v?"void":H.A(a.ret,a0)
if("args" in a){j=a.args
for(n=j.length,i="",h="",g=0;g<n;++g,h=b){f=j[g]
i=i+h+H.A(f,a0)}}else{i=""
h=""}if("opt" in a){e=a.opt
i+=h+"["
for(n=e.length,h="",g=0;g<n;++g,h=b){f=e[g]
i=i+h+H.A(f,a0)}i+="]"}if("named" in a){d=a.named
i+=h+"{"
for(n=H.cS(d),m=n.length,h="",g=0;g<m;++g,h=b){c=H.C(n[g])
i=i+h+H.A(d[c],a0)+(" "+H.a(c))}i+="}"}if(t!=null)a0.length=t
return p+"("+i+") => "+k},
bw:function(a,b,c){var u,t,s,r,q,p
if(a==null)return""
u=new P.a7("")
for(t=b,s="",r=!0,q="";t<a.length;++t,s=", "){u.a=q+s
p=a[t]
if(p!=null)r=!1
q=u.a+=H.A(p,c)}return"<"+u.h(0)+">"},
ac:function(a,b){if(a==null)return b
a=a.apply(null,b)
if(a==null)return
if(typeof a==="object"&&a!==null&&a.constructor===Array)return a
if(typeof a=="function")return a.apply(null,b)
return b},
W:function(a,b,c,d){var u,t
if(a==null)return!1
u=H.Y(a)
t=J.q(a)
if(t[b]==null)return!1
return H.bW(H.ac(t[d],u),null,c,null)},
cM:function(a,b,c,d){if(a==null)return a
if(H.W(a,b,c,d))return a
throw H.b(H.z(a,function(e,f){return e.replace(/[^<,> ]+/g,function(g){return f[g]||g})}(H.M(b.substring(2))+H.bw(c,0,null),v.mangledGlobalNames)))},
bW:function(a,b,c,d){var u,t
if(c==null)return!0
if(a==null){u=c.length
for(t=0;t<u;++t)if(!H.o(null,null,c[t],d))return!1
return!0}u=a.length
for(t=0;t<u;++t)if(!H.o(a[t],b,c[t],d))return!1
return!0},
ds:function(a,b,c){return a.apply(b,H.ac(J.q(b)["$a"+H.a(c)],H.Y(b)))},
c1:function(a){var u
if(typeof a==="number")return!1
if('futureOr' in a){u="type" in a?a.type:null
return a==null||a.name==="f"||a.name==="d"||a===-1||a===-2||H.c1(u)}return!1},
by:function(a,b){var u,t
if(a==null)return b==null||b.name==="f"||b.name==="d"||b===-1||b===-2||H.c1(b)
if(b==null||b===-1||b.name==="f"||b===-2)return!0
if(typeof b=="object"){if('futureOr' in b)if(H.by(a,"type" in b?b.type:null))return!0
if('func' in b)return H.aa(a,b)}u=J.q(a).constructor
t=H.Y(a)
if(t!=null){t=t.slice()
t.splice(0,0,u)
u=t}return H.o(u,null,b,null)},
p:function(a,b){if(a!=null&&!H.by(a,b))throw H.b(H.z(a,H.bm(b)))
return a},
o:function(a,b,c,d){var u,t,s,r,q,p,o,n,m,l=null
if(a===c)return!0
if(c==null||c===-1||c.name==="f"||c===-2)return!0
if(a===-2)return!0
if(a==null||a===-1||a.name==="f"||a===-2){if(typeof c==="number")return!1
if('futureOr' in c)return H.o(a,b,"type" in c?c.type:l,d)
return!1}if(typeof a==="number")return H.o(b[H.L(a)],b,c,d)
if(typeof c==="number")return!1
if(a.name==="d")return!0
u=typeof a==="object"&&a!==null&&a.constructor===Array
t=u?a[0]:a
if('futureOr' in c){s="type" in c?c.type:l
if('futureOr' in a)return H.o("type" in a?a.type:l,b,s,d)
else if(H.o(a,b,s,d))return!0
else{if(!('$i'+"n" in t.prototype))return!1
r=t.prototype["$a"+"n"]
q=H.ac(r,u?a.slice(1):l)
return H.o(typeof q==="object"&&q!==null&&q.constructor===Array?q[0]:l,b,s,d)}}if('func' in c)return H.bS(a,b,c,d)
if('func' in a)return c.name==="bp"
p=typeof c==="object"&&c!==null&&c.constructor===Array
o=p?c[0]:c
if(o!==t){n=o.name
if(!('$i'+n in t.prototype))return!1
m=t.prototype["$a"+n]}else m=l
if(!p)return!0
u=u?a.slice(1):l
p=c.slice(1)
return H.bW(H.ac(m,u),b,p,d)},
bS:function(a,b,c,d){var u,t,s,r,q,p,o,n,m,l,k,j,i,h,g
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
return H.d1(h,b,g,d)},
d1:function(a,b,c,d){var u,t,s,r=Object.getOwnPropertyNames(c)
for(u=r.length,t=0;t<u;++t){s=r[t]
if(!Object.hasOwnProperty.call(a,s))return!1
if(!H.o(c[s],d,a[s],b))return!1}return!0},
dt:function(a,b,c){Object.defineProperty(a,b,{value:c,enumerable:false,writable:true,configurable:true})},
d_:function(a){var u,t,s,r,q=H.C($.c0.$1(a)),p=$.bc[q]
if(p!=null){Object.defineProperty(a,v.dispatchPropertyName,{value:p,enumerable:false,writable:true,configurable:true})
return p.i}u=$.bh[q]
if(u!=null)return u
t=v.interceptorsByTag[q]
if(t==null){q=H.C($.bV.$2(a,q))
if(q!=null){p=$.bc[q]
if(p!=null){Object.defineProperty(a,v.dispatchPropertyName,{value:p,enumerable:false,writable:true,configurable:true})
return p.i}u=$.bh[q]
if(u!=null)return u
t=v.interceptorsByTag[q]}}if(t==null)return
u=t.prototype
s=q[0]
if(s==="!"){p=H.bj(u)
$.bc[q]=p
Object.defineProperty(a,v.dispatchPropertyName,{value:p,enumerable:false,writable:true,configurable:true})
return p.i}if(s==="~"){$.bh[q]=u
return u}if(s==="-"){r=H.bj(u)
Object.defineProperty(Object.getPrototypeOf(a),v.dispatchPropertyName,{value:r,enumerable:false,writable:true,configurable:true})
return r.i}if(s==="+")return H.c2(a,u)
if(s==="*")throw H.b(P.bP(q))
if(v.leafTags[q]===true){r=H.bj(u)
Object.defineProperty(Object.getPrototypeOf(a),v.dispatchPropertyName,{value:r,enumerable:false,writable:true,configurable:true})
return r.i}else return H.c2(a,u)},
c2:function(a,b){var u=Object.getPrototypeOf(a)
Object.defineProperty(u,v.dispatchPropertyName,{value:J.bC(b,u,null,null),enumerable:false,writable:true,configurable:true})
return b},
bj:function(a){return J.bC(a,!1,null,!!a.$idc)},
d0:function(a,b,c){var u=b.prototype
if(v.leafTags[a]===true)return H.bj(u)
else return J.bC(u,c,null,null)},
cX:function(){if(!0===$.bA)return
$.bA=!0
H.cY()},
cY:function(){var u,t,s,r,q,p,o,n
$.bc=Object.create(null)
$.bh=Object.create(null)
H.cW()
u=v.interceptorsByTag
t=Object.getOwnPropertyNames(u)
if(typeof window!="undefined"){window
s=function(){}
for(r=0;r<t.length;++r){q=t[r]
p=$.c3.$1(q)
if(p!=null){o=H.d0(q,u[q],p)
if(o!=null){Object.defineProperty(p,v.dispatchPropertyName,{value:o,enumerable:false,writable:true,configurable:true})
s.prototype=p}}}}for(r=0;r<t.length;++r){q=t[r]
if(/^[A-Za-z_]/.test(q)){n=u[q]
u["!"+q]=n
u["~"+q]=n
u["-"+q]=n
u["+"+q]=n
u["*"+q]=n}}},
cW:function(){var u,t,s,r,q,p,o=C.i()
o=H.I(C.j,H.I(C.k,H.I(C.d,H.I(C.d,H.I(C.l,H.I(C.m,H.I(C.n(C.c),o)))))))
if(typeof dartNativeDispatchHooksTransformer!="undefined"){u=dartNativeDispatchHooksTransformer
if(typeof u=="function")u=[u]
if(u.constructor==Array)for(t=0;t<u.length;++t){s=u[t]
if(typeof s=="function")o=s(o)||o}}r=o.getTag
q=o.getUnknownTag
p=o.prototypeForTag
$.c0=new H.be(r)
$.bV=new H.bf(q)
$.c3=new H.bg(p)},
I:function(a,b){return a(b)||b},
d5:function(a){if(/[[\]{}()*+?.\\^$|]/.test(a))return a.replace(/[[\]{}()*+?.\\^$|]/g,"\\$&")
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
P:function P(a,b){this.a=a
this.b=b},
bn:function bn(a){this.a=a},
a9:function a9(a){this.a=a
this.b=null},
O:function O(){},
az:function az(){},
ay:function ay(){},
a1:function a1(a,b,c,d){var _=this
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
cS:function(a){return J.bL(H.bD(a?Object.keys(a):[],[null]))},
d9:function(a){return v.mangledGlobalNames[a]},
d2:function(a){if(typeof dartPrint=="function"){dartPrint(a)
return}if(typeof console=="object"&&typeof console.log!="undefined"){console.log(a)
return}if(typeof window=="object")return
if(typeof print=="function"){print(a)
return}throw"Unable to print message: "+String(a)}},J={
bC:function(a,b,c,d){return{i:a,p:b,e:c,x:d}},
cU:function(a){var u,t,s,r,q=a[v.dispatchPropertyName]
if(q==null)if($.bA==null){H.cX()
q=a[v.dispatchPropertyName]}if(q!=null){u=q.p
if(!1===u)return q.i
if(!0===u)return a
t=Object.getPrototypeOf(a)
if(u===t)return q.i
if(q.e===t)throw H.b(P.bP("Return interceptor for "+H.a(u(a,q))))}s=a.constructor
r=s==null?null:s[$.bE()]
if(r!=null)return r
r=H.d_(a)
if(r!=null)return r
if(typeof a=="function")return C.q
u=Object.getPrototypeOf(a)
if(u==null)return C.h
if(u===Object.prototype)return C.h
if(typeof s=="function"){Object.defineProperty(s,$.bE(),{value:C.b,enumerable:false,writable:true,configurable:true})
return C.b}return C.b},
bL:function(a){a.fixed$length=Array
return a},
q:function(a){if(typeof a=="number"){if(Math.floor(a)==a)return J.a2.prototype
return J.ao.prototype}if(typeof a=="string")return J.Q.prototype
if(a==null)return J.ap.prototype
if(typeof a=="boolean")return J.an.prototype
if(a.constructor==Array)return J.E.prototype
if(typeof a!="object"){if(typeof a=="function")return J.a3.prototype
return a}if(a instanceof P.f)return a
return J.cU(a)},
cT:function(a){if(typeof a=="string")return J.Q.prototype
if(a==null)return a
if(a.constructor==Array)return J.E.prototype
if(!(a instanceof P.f))return J.S.prototype
return a},
bG:function(a){return J.cT(a).gn(a)},
ae:function(a){return J.q(a).h(a)},
i:function i(){},
an:function an(){},
ap:function ap(){},
a4:function a4(){},
au:function au(){},
S:function S(){},
a3:function a3(){},
E:function E(a){this.$ti=a},
bq:function bq(a){this.$ti=a},
af:function af(a,b,c){var _=this
_.a=a
_.b=b
_.c=0
_.d=null
_.$ti=c},
aq:function aq(){},
a2:function a2(){},
ao:function ao(){},
Q:function Q(){}},P={
cq:function(){var u,t,s={}
if(self.scheduleImmediate!=null)return P.cO()
if(self.MutationObserver!=null&&self.document!=null){u=self.document.createElement("div")
t=self.document.createElement("span")
s.a=null
new self.MutationObserver(H.X(new P.aK(s),1)).observe(u,{childList:true})
return new P.aJ(s,u,t)}else if(self.setImmediate!=null)return P.cP()
return P.cQ()},
cr:function(a){self.scheduleImmediate(H.X(new P.aL(H.c(a,{func:1,ret:-1})),0))},
cs:function(a){self.setImmediate(H.X(new P.aM(H.c(a,{func:1,ret:-1})),0))},
ct:function(a){H.c(a,{func:1,ret:-1})
P.cu(0,a)},
cu:function(a,b){var u=new P.b5()
u.O(a,b)
return u},
cC:function(a){return new P.aH(new P.j($.e,[a]),[a])},
cy:function(a,b){a.$2(0,null)
b.b=!0
return b.a},
cv:function(a,b){P.cz(a,b)},
cx:function(a,b){b.u(a)},
cw:function(a,b){b.v(H.a0(a),H.Z(a))},
cz:function(a,b){var u,t=null,s=new P.b8(b),r=new P.b9(b),q=J.q(a)
if(!!q.$ij)a.H(s,r,t)
else if(!!q.$in)a.B(s,r,t)
else{u=new P.j($.e,[null])
H.p(a,null)
u.a=4
u.c=a
u.H(s,t,t)}},
cK:function(a){var u=function(b,c){return function(d,e){while(true)try{b(d,e)
break}catch(t){e=t
d=c}}}(a,1)
return $.e.K(new P.bb(u),P.d,P.B,null)},
bR:function(a,b){var u,t,s
b.a=1
try{a.B(new P.aT(b),new P.aU(b),P.d)}catch(s){u=H.a0(s)
t=H.Z(s)
P.d6(new P.aV(b,u,t))}},
aS:function(a,b){var u,t
for(;u=a.a,u===2;)a=H.h(a.c,"$ij")
if(u>=4){t=b.l()
b.a=a.a
b.c=a.c
P.F(b,t)}else{t=H.h(b.c,"$it")
b.a=2
b.c=a
a.G(t)}},
F:function(a,b){var u,t,s,r,q,p,o,n,m,l,k,j,i=null,h={},g=h.a=a
for(;!0;){u={}
t=g.a===8
if(b==null){if(t){s=H.h(g.c,"$il")
P.bx(i,i,g.b,s.a,s.b)}return}for(;r=b.a,r!=null;b=r){b.a=null
P.F(h.a,b)}g=h.a
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
P.bx(i,i,g.b,q.a,q.b)
return}l=$.e
if(l!==n)$.e=n
else l=i
g=b.c
if((g&15)===8)new P.b_(h,u,b,t).$0()
else if(p){if((g&1)!==0)new P.aZ(u,b,q).$0()}else if((g&2)!==0)new P.aY(h,u,b).$0()
if(l!=null)$.e=l
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
cE:function(a,b){if(H.aa(a,{func:1,args:[P.f,P.k]}))return b.K(a,null,P.f,P.k)
if(H.aa(a,{func:1,args:[P.f]}))return H.c(a,{func:1,ret:null,args:[P.f]})
throw H.b(P.bH(a,"onError","Error handler must accept one Object or one Object and a StackTrace as arguments, and return a a valid result"))},
cD:function(){var u,t
for(;u=$.G,u!=null;){$.U=null
t=u.b
$.G=t
if(t==null)$.T=null
u.a.$0()}},
cI:function(){$.bv=!0
try{P.cD()}finally{$.U=null
$.bv=!1
if($.G!=null)$.bF().$1(P.bX())}},
bU:function(a){var u=new P.a8(a)
if($.G==null){$.G=$.T=u
if(!$.bv)$.bF().$1(P.bX())}else $.T=$.T.b=u},
cH:function(a){var u,t,s=$.G
if(s==null){P.bU(a)
$.U=$.T
return}u=new P.a8(a)
t=$.U
if(t==null){u.b=s
$.G=$.U=u}else{u.b=t.b
$.U=t.b=u
if(u.b==null)$.T=u}},
d6:function(a){var u=null,t=$.e
if(C.a===t){P.H(u,u,C.a,a)
return}P.H(u,u,t,H.c(t.J(a),{func:1,ret:-1}))},
dd:function(a,b){H.ad(new P.w(!1,null,"stream","Must not be null"))
return new P.b4([b])},
bx:function(a,b,c,d,e){var u={}
u.a=d
P.cH(new P.ba(u,e))},
bT:function(a,b,c,d,e){var u,t=$.e
if(t===c)return d.$0()
$.e=c
u=t
try{t=d.$0()
return t}finally{$.e=u}},
cG:function(a,b,c,d,e,f,g){var u,t=$.e
if(t===c)return d.$1(e)
$.e=c
u=t
try{t=d.$1(e)
return t}finally{$.e=u}},
cF:function(a,b,c,d,e,f,g,h,i){var u,t=$.e
if(t===c)return d.$2(e,f)
$.e=c
u=t
try{t=d.$2(e,f)
return t}finally{$.e=u}},
H:function(a,b,c,d){var u
H.c(d,{func:1,ret:-1})
u=C.a!==c
if(u)d=!(!u||!1)?c.J(d):c.U(d,-1)
P.bU(d)},
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
cl:function(a){if(a instanceof H.O)return a.h(0)
return"Instance of '"+H.a(H.a5(a))+"'"},
cp:function(a,b,c){var u=new J.af(b,b.length,[H.m(b,0)])
if(!u.w())return a
if(c.length===0){do a+=H.a(u.d)
while(u.w())}else{a+=H.a(u.d)
for(;u.w();)a=a+c+H.a(u.d)}return a},
al:function(a){if(typeof a==="number"||typeof a==="boolean"||null==a)return J.ae(a)
if(typeof a==="string")return JSON.stringify(a)
return P.cl(a)},
bH:function(a,b,c){return new P.w(!0,a,b,c)},
bt:function(a,b){return new P.av(!0,a,b,"Value not in range")},
bQ:function(a){return new P.aF(a)},
bP:function(a){return new P.aD(a)},
bN:function(a){return new P.ax(a)},
J:function J(){},
bd:function bd(){},
D:function D(){},
ag:function ag(){},
R:function R(){},
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
B:function B(){},
as:function as(){},
d:function d(){},
a_:function a_(){},
f:function f(){},
k:function k(){},
r:function r(){},
a7:function a7(a){this.a=a},
d3:function(a,b){var u=new P.j($.e,[b]),t=new P.aI(u,[b])
a.then(H.X(new P.bk(t,b),1),H.X(new P.bl(t),1))
return u},
bk:function bk(a,b){this.a=a
this.b=b},
bl:function bl(a){this.a=a},
cn:function(a,b,c){var u,t
if(P.cB(a))return b+"..."+c
u=new P.a7(b)
C.e.I($.V,a)
try{t=u
t.a=P.cp(t.a,a,", ")}finally{if(0>=$.V.length)return H.bB($.V,-1)
$.V.pop()}u.a+=c
t=u.a
return t.charCodeAt(0)==0?t:t},
cB:function(a){var u,t
for(u=$.V.length,t=0;t<u;++t)if(a===$.V[t])return!0
return!1}},W={ak:function ak(){},x:function x(){},y:function y(){}},M={
ab:function(){var u=0,t=P.cC(null),s
var $async$ab=P.cK(function(a,b){if(a===1)return P.cw(b,t)
while(true)switch(u){case 0:s=window.navigator.serviceWorker
u=2
return P.cv(P.d3(s.register("/sw.js",null),W.y).M(new M.bi(),P.d),$async$ab)
case 2:return P.cx(null,t)}})
return P.cy($async$ab,t)},
bi:function bi(){}}
var w=[C,H,J,P,W,M]
hunkHelpers.setFunctionNamesIfNecessary(w)
var $={}
H.br.prototype={}
J.i.prototype={
h:function(a){return"Instance of '"+H.a(H.a5(a))+"'"}}
J.an.prototype={
h:function(a){return String(a)},
$iJ:1}
J.ap.prototype={
h:function(a){return"null"},
$id:1}
J.a4.prototype={
h:function(a){return String(a)}}
J.au.prototype={}
J.S.prototype={}
J.a3.prototype={
h:function(a){var u=a[$.c5()]
if(u==null)return this.N(a)
return"JavaScript function for "+H.a(J.ae(u))},
$S:function(){return{func:1,opt:[,,,,,,,,,,,,,,,,]}},
$ibp:1}
J.E.prototype={
I:function(a,b){H.p(b,H.m(a,0))
if(!!a.fixed$length)H.ad(P.bQ("add"))
a.push(b)},
h:function(a){return P.cn(a,"[","]")},
gn:function(a){return a.length},
$icm:1}
J.bq.prototype={}
J.af.prototype={
w:function(){var u,t=this,s=t.a,r=s.length
if(t.b!==r)throw H.b(H.d7(s))
u=t.c
if(u>=r){t.sF(null)
return!1}t.sF(s[u]);++t.c
return!0},
sF:function(a){this.d=H.p(a,H.m(this,0))}}
J.aq.prototype={
h:function(a){if(a===0&&1/a<0)return"-0.0"
else return""+a},
T:function(a,b){var u
if(a>0)u=this.S(a,b)
else{u=b>31?31:b
u=a>>u>>>0}return u},
S:function(a,b){return b>31?0:a>>>b},
$ia_:1}
J.a2.prototype={$iB:1}
J.ao.prototype={}
J.Q.prototype={
R:function(a,b){if(b>=a.length)throw H.b(H.bY(a,b))
return a.charCodeAt(b)},
j:function(a,b){if(typeof b!=="string")throw H.b(P.bH(b,null,null))
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
H.P.prototype={}
H.bn.prototype={
$1:function(a){if(!!J.q(a).$iD)if(a.$thrownJsError==null)a.$thrownJsError=this.a
return a},
$S:4}
H.a9.prototype={
h:function(a){var u,t=this.b
if(t!=null)return t
t=this.a
u=t!==null&&typeof t==="object"?t.stack:null
return this.b=u==null?"":u},
$ik:1}
H.O.prototype={
h:function(a){var u=this.constructor,t=u==null?null:u.name
return"Closure '"+H.M(t==null?"unknown":t)+"'"},
$ibp:1,
ga_:function(){return this},
$C:"$1",
$R:1,
$D:null}
H.az.prototype={}
H.ay.prototype={
h:function(a){var u=this.$static_name
if(u==null)return"Closure of unknown static method"
return"Closure '"+H.M(u)+"'"}}
H.a1.prototype={
h:function(a){var u=this.c
if(u==null)u=this.a
return"Closure '"+H.a(this.d)+"' of "+("Instance of '"+H.a(H.a5(u))+"'")}}
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
$1:function(a){return this.a(H.C(a))},
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
O:function(a,b){if(self.setTimeout!=null)self.setTimeout(H.X(new P.b6(this,b),0),a)
else throw H.b(P.bQ("`setTimeout()` not found."))}}
P.b6.prototype={
$0:function(){this.b.$0()},
$S:1}
P.aH.prototype={
u:function(a){var u,t,s=this,r=H.m(s,0)
H.K(a,{futureOr:1,type:r})
u=!s.b||H.W(a,"$in",s.$ti,"$an")
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
$2:function(a,b){this.a.$2(1,new H.P(a,H.h(b,"$ik")))},
$S:9}
P.bb.prototype={
$2:function(a,b){this.a(H.L(a),b)},
$S:10}
P.aN.prototype={
v:function(a,b){var u
if(a==null)a=new P.R()
u=this.a
if(u.a!==0)throw H.b(P.bN("Future already completed"))
u.D(a,b)},
V:function(a){return this.v(a,null)}}
P.aI.prototype={
u:function(a){var u
H.K(a,{futureOr:1,type:H.m(this,0)})
u=this.a
if(u.a!==0)throw H.b(P.bN("Future already completed"))
u.C(a)}}
P.t.prototype={
X:function(a){if((this.c&15)!==6)return!0
return this.b.b.A(H.c(this.d,{func:1,ret:P.J,args:[P.f]}),a.a,P.J,P.f)},
W:function(a){var u=this.e,t=P.f,s={futureOr:1,type:H.m(this,1)},r=this.b.b
if(H.aa(u,{func:1,args:[P.f,P.k]}))return H.K(r.Y(u,a.a,a.b,null,t,P.k),s)
else return H.K(r.A(H.c(u,{func:1,args:[P.f]}),a.a,null,t),s)}}
P.j.prototype={
B:function(a,b,c){var u,t,s,r=H.m(this,0)
H.c(a,{func:1,ret:{futureOr:1,type:c},args:[r]})
u=$.e
if(u!==C.a){H.c(a,{func:1,ret:{futureOr:1,type:c},args:[r]})
if(b!=null)b=P.cE(b,u)}t=new P.j($.e,[c])
s=b==null?1:3
this.p(new P.t(t,s,a,b,[r,c]))
return t},
M:function(a,b){return this.B(a,null,b)},
H:function(a,b,c){var u,t=H.m(this,0)
H.c(a,{func:1,ret:{futureOr:1,type:c},args:[t]})
u=new P.j($.e,[c])
this.p(new P.t(u,(b==null?1:3)|16,a,b,[t,c]))
return u},
p:function(a){var u,t=this,s=t.a
if(s<=1){a.a=H.h(t.c,"$it")
t.c=a}else{if(s===2){u=H.h(t.c,"$ij")
s=u.a
if(s<4){u.p(a)
return}t.a=s
t.c=u.c}P.H(null,null,t.b,H.c(new P.aP(t,a),{func:1,ret:-1}))}},
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
P.H(null,null,p.b,H.c(new P.aX(o,p),{func:1,ret:-1}))}},
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
P.F(t,u)},
k:function(a,b){var u,t=this
H.h(b,"$ik")
u=t.l()
t.a=8
t.c=new P.l(a,b)
P.F(t,u)},
C:function(a){var u=this
H.K(a,{futureOr:1,type:H.m(u,0)})
if(H.W(a,"$in",u.$ti,"$an")){u.P(a)
return}u.a=1
P.H(null,null,u.b,H.c(new P.aR(u,a),{func:1,ret:-1}))},
P:function(a){var u=this,t=u.$ti
H.cM(a,"$in",t,"$an")
if(H.W(a,"$ij",t,null)){if(a.a===8){u.a=1
P.H(null,null,u.b,H.c(new P.aW(u,a),{func:1,ret:-1}))}else P.aS(a,u)
return}P.bR(a,u)},
D:function(a,b){this.a=1
P.H(null,null,this.b,H.c(new P.aQ(this,a,b),{func:1,ret:-1}))},
$in:1}
P.aP.prototype={
$0:function(){P.F(this.a,this.b)},
$S:0}
P.aX.prototype={
$0:function(){P.F(this.b,this.a.a)},
$S:0}
P.aT.prototype={
$1:function(a){var u,t,s=this.a
s.a=0
u=H.m(s,0)
H.K(a,{futureOr:1,type:u})
if(H.W(a,"$in",[u],"$an"))if(H.W(a,"$ij",[u],null))P.aS(a,s)
else P.bR(a,s)
else{t=s.l()
H.p(a,u)
s.a=4
s.c=a
P.F(s,t)}},
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
n=s.b.b.L(H.c(s.d,{func:1}),null)}catch(r){u=H.a0(r)
t=H.Z(r)
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
s.b=n.M(new P.b0(p),null)
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
n.a.b=s.b.b.A(H.c(s.d,{func:1,ret:{futureOr:1,type:p},args:[r]}),q,{futureOr:1,type:p},r)}catch(o){u=H.a0(o)
t=H.Z(o)
s=n.a
s.b=new P.l(u,t)
s.a=!0}},
$S:1}
P.aY.prototype={
$0:function(){var u,t,s,r,q,p,o,n,m=this
try{u=H.h(m.a.a.c,"$il")
r=m.c
if(H.cR(r.X(u))&&r.e!=null){q=m.b
q.b=r.W(u)
q.a=!1}}catch(p){t=H.a0(p)
s=H.Z(p)
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
$iD:1}
P.b7.prototype={$idp:1}
P.ba.prototype={
$0:function(){var u,t=this.a,s=t.a
t=s==null?t.a=new P.R():s
s=this.b
if(s==null)throw H.b(t)
u=H.b(t)
u.stack=s.h(0)
throw u},
$S:0}
P.b1.prototype={
Z:function(a){var u,t,s,r=null
H.c(a,{func:1,ret:-1})
try{if(C.a===$.e){a.$0()
return}P.bT(r,r,this,a,-1)}catch(s){u=H.a0(s)
t=H.Z(s)
P.bx(r,r,this,u,H.h(t,"$ik"))}},
U:function(a,b){return new P.b3(this,H.c(a,{func:1,ret:b}),b)},
J:function(a){return new P.b2(this,H.c(a,{func:1,ret:-1}))},
L:function(a,b){H.c(a,{func:1,ret:b})
if($.e===C.a)return a.$0()
return P.bT(null,null,this,a,b)},
A:function(a,b,c,d){H.c(a,{func:1,ret:c,args:[d]})
H.p(b,d)
if($.e===C.a)return a.$1(b)
return P.cG(null,null,this,a,b,c,d)},
Y:function(a,b,c,d,e,f){H.c(a,{func:1,ret:d,args:[e,f]})
H.p(b,e)
H.p(c,f)
if($.e===C.a)return a.$2(b,c)
return P.cF(null,null,this,a,b,c,d,e,f)},
K:function(a,b,c,d){return H.c(a,{func:1,ret:b,args:[c,d]})}}
P.b3.prototype={
$0:function(){return this.a.L(this.b,this.c)},
$S:function(){return{func:1,ret:this.c}}}
P.b2.prototype={
$0:function(){return this.a.Z(this.b)},
$S:1}
P.J.prototype={}
P.bd.prototype={}
P.D.prototype={}
P.ag.prototype={
h:function(a){return"Assertion failed"}}
P.R.prototype={
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
gq:function(){var u,t=H.L(this.b)
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
$iD:1}
P.aj.prototype={
h:function(a){var u=this.a
return u==null?"Reading static variable during its initialization":"Reading static variable '"+u+"' during its initialization"}}
P.aO.prototype={
h:function(a){return"Exception: "+this.a}}
P.B.prototype={}
P.as.prototype={$icm:1}
P.d.prototype={
h:function(a){return"null"}}
P.a_.prototype={}
P.f.prototype={constructor:P.f,$if:1,
h:function(a){return"Instance of '"+H.a(H.a5(this))+"'"},
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
W.y.prototype={$iy:1}
P.bk.prototype={
$1:function(a){return this.a.u(H.K(a,{futureOr:1,type:this.b}))},
$S:2}
P.bl.prototype={
$1:function(a){return this.a.V(a)},
$S:2}
M.bi.prototype={
$1:function(a){H.h(a,"$iy")
H.d2("Registred")},
$S:13};(function aliases(){var u=J.a4.prototype
u.N=u.h})();(function installTearOffs(){var u=hunkHelpers._static_1,t=hunkHelpers._static_0
u(P,"cO","cr",3)
u(P,"cP","cs",3)
u(P,"cQ","ct",3)
t(P,"bX","cI",1)})();(function inheritance(){var u=hunkHelpers.inherit,t=hunkHelpers.inheritMany
u(P.f,null)
t(P.f,[H.br,J.i,J.af,H.aA,P.D,H.P,H.O,H.a9,P.b5,P.aH,P.aN,P.t,P.j,P.a8,P.b4,P.l,P.b7,P.J,P.a_,P.a6,P.aO,P.as,P.d,P.k,P.r,P.a7])
t(J.i,[J.an,J.ap,J.a4,J.E,J.aq,J.Q,W.ak,W.x])
t(J.a4,[J.au,J.S,J.a3])
u(J.bq,J.E)
t(J.aq,[J.a2,J.ao])
t(P.D,[H.at,H.ar,H.aE,H.aC,H.aw,P.ag,P.R,P.w,P.aF,P.aD,P.ax,P.ai,P.aj])
t(H.O,[H.bn,H.az,H.be,H.bf,H.bg,P.aK,P.aJ,P.aL,P.aM,P.b6,P.b8,P.b9,P.bb,P.aP,P.aX,P.aT,P.aU,P.aV,P.aR,P.aW,P.aQ,P.b_,P.b0,P.aZ,P.aY,P.ba,P.b3,P.b2,P.bk,P.bl,M.bi])
t(H.az,[H.ay,H.a1])
u(H.aG,P.ag)
u(P.aI,P.aN)
u(P.b1,P.b7)
t(P.a_,[P.bd,P.B])
t(P.w,[P.av,P.am])
u(W.y,W.x)})()
var v={mangledGlobalNames:{B:"int",bd:"double",a_:"num",r:"String",J:"bool",d:"Null",as:"List"},mangledNames:{},getTypeFromName:getGlobalFromName,metadata:[],types:[{func:1,ret:P.d},{func:1,ret:-1},{func:1,ret:-1,args:[,]},{func:1,ret:-1,args:[{func:1,ret:-1}]},{func:1,args:[,]},{func:1,ret:P.d,args:[,]},{func:1,args:[,P.r]},{func:1,args:[P.r]},{func:1,ret:P.d,args:[{func:1,ret:-1}]},{func:1,ret:P.d,args:[,P.k]},{func:1,ret:P.d,args:[P.B,,]},{func:1,ret:P.d,args:[,],opt:[P.k]},{func:1,ret:[P.j,,],args:[,]},{func:1,ret:P.d,args:[W.y]}],interceptorsByTag:null,leafTags:null};(function constants(){C.o=J.i.prototype
C.e=J.E.prototype
C.p=J.a2.prototype
C.f=J.Q.prototype
C.q=J.a3.prototype
C.h=J.au.prototype
C.b=J.S.prototype
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
$.N=null
$.bI=null
$.bu=!1
$.c0=null
$.bV=null
$.c3=null
$.bc=null
$.bh=null
$.bA=null
$.G=null
$.T=null
$.U=null
$.bv=!1
$.e=C.a
$.V=[]})();(function lazyInitializers(){var u=hunkHelpers.lazy
u($,"da","c5",function(){return H.c_("_$dart_dartClosure")})
u($,"db","bE",function(){return H.c_("_$dart_js")})
u($,"de","c6",function(){return H.v(H.aB({
toString:function(){return"$receiver$"}}))})
u($,"df","c7",function(){return H.v(H.aB({$method$:null,
toString:function(){return"$receiver$"}}))})
u($,"dg","c8",function(){return H.v(H.aB(null))})
u($,"dh","c9",function(){return H.v(function(){var $argumentsExpr$='$arguments$'
try{null.$method$($argumentsExpr$)}catch(t){return t.message}}())})
u($,"dk","cc",function(){return H.v(H.aB(void 0))})
u($,"dl","cd",function(){return H.v(function(){var $argumentsExpr$='$arguments$'
try{(void 0).$method$($argumentsExpr$)}catch(t){return t.message}}())})
u($,"dj","cb",function(){return H.v(H.bO(null))})
u($,"di","ca",function(){return H.v(function(){try{null.$method$}catch(t){return t.message}}())})
u($,"dn","cf",function(){return H.v(H.bO(void 0))})
u($,"dm","ce",function(){return H.v(function(){try{(void 0).$method$}catch(t){return t.message}}())})
u($,"dq","bF",function(){return P.cq()})})();(function nativeSupport(){!function(){var u=function(a){var o={}
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
