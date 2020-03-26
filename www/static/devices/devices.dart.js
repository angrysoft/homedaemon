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
a[c]=function(){a[c]=function(){H.cU(b)}
var t
var s=d
try{if(a[b]===u){t=a[b]=s
t=a[b]=d()}else t=a[b]}finally{if(t===s)a[b]=null
a[c]=function(){return this[b]}}return t}}function makeConstList(a){a.immutable$list=Array
a.fixed$length=Array
return a}function convertToFastObject(a){function t(){}t.prototype=a
new t()
return a}function convertAllToFastObject(a){for(var u=0;u<a.length;++u)convertToFastObject(a[u])}var y=0
function tearOffGetter(a,b,c,d,e){return e?new Function("funcs","applyTrampolineIndex","reflectionInfo","name","H","c","return function tearOff_"+d+y+++"(receiver) {"+"if (c === null) c = "+"H.br"+"("+"this, funcs, applyTrampolineIndex, reflectionInfo, false, true, name);"+"return new c(this, funcs[0], receiver, name);"+"}")(a,b,c,d,H,null):new Function("funcs","applyTrampolineIndex","reflectionInfo","name","H","c","return function tearOff_"+d+y+++"() {"+"if (c === null) c = "+"H.br"+"("+"this, funcs, applyTrampolineIndex, reflectionInfo, false, false, name);"+"return new c(this, funcs[0], null, name);"+"}")(a,b,c,d,H,null)}function tearOff(a,b,c,d,e,f){var u=null
return d?function(){if(u===null)u=H.br(this,a,b,c,true,false,e).prototype
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
if(w[u][a])return w[u][a]}}var C={},H={bj:function bj(){},
I:function(a){var u,t=H.cV(a)
if(typeof t==="string")return t
u="minified:"+a
return u},
cH:function(a){return v.types[H.U(a)]},
a:function(a){var u
if(typeof a==="string")return a
if(typeof a==="number"){if(a!==0)return""+a}else if(!0===a)return"true"
else if(!1===a)return"false"
else if(a==null)return"null"
u=J.ac(a)
if(typeof u!=="string")throw H.c(H.cx(a))
return u},
a0:function(a){return H.ch(a)+H.bo(H.T(a),0,null)},
ch:function(a){var u,t,s,r,q,p,o,n,m=null,l=J.p(a),k=l.constructor
if(typeof k=="function"){u=k.name
t=typeof u==="string"?u:m}else t=m
s=t==null
if(s||l===C.o||!!l.$iN){r=C.c(a)
if(s)t=r
if(r==="Object"){q=a.constructor
if(typeof q=="function"){p=String(q).match(/^\s*function\s*([\w$]*)\s*\(/)
o=p==null?m:p[1]
if(typeof o==="string"&&/^\w+$/.test(o))t=o}}return t}t=t
n=t.length
if(n>1&&C.f.K(t,0)===36){if(1>n)H.W(P.bl(1,m))
if(n>n)H.W(P.bl(n,m))
t=t.substring(1,n)}return H.I(t)},
bt:function(a,b){if(a==null)J.by(a)
throw H.c(H.bQ(a,b))},
bQ:function(a,b){var u,t="index"
if(typeof b!=="number"||Math.floor(b)!==b)return new P.w(!0,b,t,null)
u=J.by(a)
if(b<0||b>=u)return new P.ak(u,!0,b,t,"Index out of range")
return P.bl(b,t)},
cx:function(a){return new P.w(!0,a,null,null)},
c:function(a){var u
if(a==null)a=new P.M()
u=new Error()
u.dartException=a
if("defineProperty" in Object){Object.defineProperty(u,"message",{get:H.bY})
u.name=""}else u.toString=H.bY
return u},
bY:function(){return J.ac(this.dartException)},
W:function(a){throw H.c(a)},
cT:function(a){throw H.c(new P.ag(a))},
t:function(a){var u,t,s,r,q,p
a=H.cR(a.replace(String({}),'$receiver$'))
u=a.match(/\\\$[a-zA-Z]+\\\$/g)
if(u==null)u=H.bv([],[P.o])
t=u.indexOf("\\$arguments\\$")
s=u.indexOf("\\$argumentsExpr\\$")
r=u.indexOf("\\$expr\\$")
q=u.indexOf("\\$method\\$")
p=u.indexOf("\\$receiver\\$")
return new H.ay(a.replace(new RegExp('\\\\\\$arguments\\\\\\$','g'),'((?:x|[^x])*)').replace(new RegExp('\\\\\\$argumentsExpr\\\\\\$','g'),'((?:x|[^x])*)').replace(new RegExp('\\\\\\$expr\\\\\\$','g'),'((?:x|[^x])*)').replace(new RegExp('\\\\\\$method\\\\\\$','g'),'((?:x|[^x])*)').replace(new RegExp('\\\\\\$receiver\\\\\\$','g'),'((?:x|[^x])*)'),t,s,r,q,p)},
az:function(a){return function($expr$){var $argumentsExpr$='$arguments$'
try{$expr$.$method$($argumentsExpr$)}catch(u){return u.message}}(a)},
bG:function(a){return function($expr$){try{$expr$.$method$}catch(u){return u.message}}(a)},
bE:function(a,b){return new H.ar(a,b==null?null:b.method)},
bk:function(a,b){var u=b==null,t=u?null:b.method
return new H.ap(a,t,u?null:b.receiver)},
ab:function(a){var u,t,s,r,q,p,o,n,m,l,k,j,i,h,g=null,f=new H.bf(a)
if(a==null)return
if(typeof a!=="object")return a
if("dartException" in a)return f.$1(a.dartException)
else if(!("message" in a))return a
u=a.message
if("number" in a&&typeof a.number=="number"){t=a.number
s=t&65535
if((C.p.M(t,16)&8191)===10)switch(s){case 438:return f.$1(H.bk(H.a(u)+" (Error "+s+")",g))
case 445:case 5007:return f.$1(H.bE(H.a(u)+" (Error "+s+")",g))}}if(a instanceof TypeError){r=$.c_()
q=$.c0()
p=$.c1()
o=$.c2()
n=$.c5()
m=$.c6()
l=$.c4()
$.c3()
k=$.c8()
j=$.c7()
i=r.i(u)
if(i!=null)return f.$1(H.bk(H.A(u),i))
else{i=q.i(u)
if(i!=null){i.method="call"
return f.$1(H.bk(H.A(u),i))}else{i=p.i(u)
if(i==null){i=o.i(u)
if(i==null){i=n.i(u)
if(i==null){i=m.i(u)
if(i==null){i=l.i(u)
if(i==null){i=o.i(u)
if(i==null){i=k.i(u)
if(i==null){i=j.i(u)
h=i!=null}else h=!0}else h=!0}else h=!0}else h=!0}else h=!0}else h=!0}else h=!0
if(h)return f.$1(H.bE(H.A(u),i))}}return f.$1(new H.aC(typeof u==="string"?u:""))}if(a instanceof RangeError){if(typeof u==="string"&&u.indexOf("call stack")!==-1)return new P.a2()
u=function(b){try{return String(b)}catch(e){}return null}(a)
return f.$1(new P.w(!1,g,g,typeof u==="string"?u.replace(/^RangeError:\s*/,""):u))}if(typeof InternalError=="function"&&a instanceof InternalError)if(typeof u==="string"&&u==="too much recursion")return new P.a2()
return a},
a8:function(a){var u
if(a==null)return new H.a5(a)
u=a.$cachedTrace
if(u!=null)return u
return a.$cachedTrace=new H.a5(a)},
cL:function(a,b,c,d,e,f){H.e(a,"$ibh")
switch(H.U(b)){case 0:return a.$0()
case 1:return a.$1(c)
case 2:return a.$2(c,d)
case 3:return a.$3(c,d,e)
case 4:return a.$4(c,d,e,f)}throw H.c(new P.aL("Unsupported number of arguments for wrapped closure"))},
R:function(a,b){var u=a.$identity
if(!!u)return u
u=function(c,d,e){return function(f,g,h,i){return e(c,d,f,g,h,i)}}(a,b,H.cL)
a.$identity=u
return u},
cd:function(a,b,c,d,e,f,g){var u,t,s,r,q,p,o,n,m=null,l=b[0],k=l.$callName,j=e?Object.create(new H.aw().constructor.prototype):Object.create(new H.X(m,m,m,m).constructor.prototype)
j.$initialize=j.constructor
if(e)u=function static_tear_off(){this.$initialize()}
else{t=$.q
if(typeof t!=="number")return t.j()
$.q=t+1
t=new Function("a,b,c,d"+t,"this.$initialize(a,b,c,d"+t+")")
u=t}j.constructor=u
u.prototype=j
if(!e){s=H.bC(a,l,f)
s.$reflectionInfo=d}else{j.$static_name=g
s=l}r=H.c9(d,e,f)
j.$S=r
j[k]=s
for(q=s,p=1;p<b.length;++p){o=b[p]
n=o.$callName
if(n!=null){o=e?o:H.bC(a,o,f)
j[n]=o}if(p===c){o.$reflectionInfo=d
q=o}}j.$C=q
j.$R=l.$R
j.$D=l.$D
return u},
c9:function(a,b,c){var u
if(typeof a=="number")return function(d,e){return function(){return d(e)}}(H.cH,a)
if(typeof a=="function")if(b)return a
else{u=c?H.bB:H.bg
return function(d,e){return function(){return d.apply({$receiver:e(this)},arguments)}}(a,u)}throw H.c("Error in functionType of tearoff")},
ca:function(a,b,c,d){var u=H.bg
switch(b?-1:a){case 0:return function(e,f){return function(){return f(this)[e]()}}(c,u)
case 1:return function(e,f){return function(g){return f(this)[e](g)}}(c,u)
case 2:return function(e,f){return function(g,h){return f(this)[e](g,h)}}(c,u)
case 3:return function(e,f){return function(g,h,i){return f(this)[e](g,h,i)}}(c,u)
case 4:return function(e,f){return function(g,h,i,j){return f(this)[e](g,h,i,j)}}(c,u)
case 5:return function(e,f){return function(g,h,i,j,k){return f(this)[e](g,h,i,j,k)}}(c,u)
default:return function(e,f){return function(){return e.apply(f(this),arguments)}}(d,u)}},
bC:function(a,b,c){var u,t,s,r,q,p,o
if(c)return H.cc(a,b)
u=b.$stubName
t=b.length
s=a[u]
r=b==null?s==null:b===s
q=!r||t>=27
if(q)return H.ca(t,!r,u,b)
if(t===0){r=$.q
if(typeof r!=="number")return r.j()
$.q=r+1
p="self"+r
r="return function(){var "+p+" = this."
q=$.J
return new Function(r+H.a(q==null?$.J=H.af("self"):q)+";return "+p+"."+H.a(u)+"();}")()}o="abcdefghijklmnopqrstuvwxyz".split("").splice(0,t).join(",")
r=$.q
if(typeof r!=="number")return r.j()
$.q=r+1
o+=r
r="return function("+o+"){return this."
q=$.J
return new Function(r+H.a(q==null?$.J=H.af("self"):q)+"."+H.a(u)+"("+o+");}")()},
cb:function(a,b,c,d){var u=H.bg,t=H.bB
switch(b?-1:a){case 0:throw H.c(new H.au("Intercepted function with no arguments."))
case 1:return function(e,f,g){return function(){return f(this)[e](g(this))}}(c,u,t)
case 2:return function(e,f,g){return function(h){return f(this)[e](g(this),h)}}(c,u,t)
case 3:return function(e,f,g){return function(h,i){return f(this)[e](g(this),h,i)}}(c,u,t)
case 4:return function(e,f,g){return function(h,i,j){return f(this)[e](g(this),h,i,j)}}(c,u,t)
case 5:return function(e,f,g){return function(h,i,j,k){return f(this)[e](g(this),h,i,j,k)}}(c,u,t)
case 6:return function(e,f,g){return function(h,i,j,k,l){return f(this)[e](g(this),h,i,j,k,l)}}(c,u,t)
default:return function(e,f,g,h){return function(){h=[g(this)]
Array.prototype.push.apply(h,arguments)
return e.apply(f(this),h)}}(d,u,t)}},
cc:function(a,b){var u,t,s,r,q,p,o,n=$.J
if(n==null)n=$.J=H.af("self")
u=$.bA
if(u==null)u=$.bA=H.af("receiver")
t=b.$stubName
s=b.length
r=a[t]
q=b==null?r==null:b===r
p=!q||s>=28
if(p)return H.cb(s,!q,t,b)
if(s===1){n="return function(){return this."+H.a(n)+"."+H.a(t)+"(this."+H.a(u)+");"
u=$.q
if(typeof u!=="number")return u.j()
$.q=u+1
return new Function(n+u+"}")()}o="abcdefghijklmnopqrstuvwxyz".split("").splice(0,s-1).join(",")
n="return function("+o+"){return this."+H.a(n)+"."+H.a(t)+"(this."+H.a(u)+", "+o+");"
u=$.q
if(typeof u!=="number")return u.j()
$.q=u+1
return new Function(n+u+"}")()},
br:function(a,b,c,d,e,f,g){return H.cd(a,b,c,d,!!e,!!f,g)},
bg:function(a){return a.a},
bB:function(a){return a.c},
af:function(a){var u,t,s,r=new H.X("self","target","receiver","name"),q=J.bD(Object.getOwnPropertyNames(r))
for(u=q.length,t=0;t<u;++t){s=q[t]
if(r[s]===a)return s}},
cD:function(a){if(a==null)H.cz("boolean expression must not be null")
return a},
A:function(a){if(a==null)return a
if(typeof a==="string")return a
throw H.c(H.y(a,"String"))},
da:function(a){if(a==null)return a
if(typeof a==="boolean")return a
throw H.c(H.y(a,"bool"))},
U:function(a){if(a==null)return a
if(typeof a==="number"&&Math.floor(a)===a)return a
throw H.c(H.y(a,"int"))},
cQ:function(a,b){throw H.c(H.y(a,H.I(H.A(b).substring(2))))},
e:function(a,b){if(a==null)return a
if((typeof a==="object"||typeof a==="function")&&J.p(a)[b])return a
H.cQ(a,b)},
bR:function(a){var u
if("$S" in a){u=a.$S
if(typeof u=="number")return v.types[H.U(u)]
else return a.$S()}return},
a7:function(a,b){var u
if(typeof a=="function")return!0
u=H.bR(J.p(a))
if(u==null)return!1
return H.bK(u,null,b,null)},
b:function(a,b){var u,t
if(a==null)return a
if($.bm)return a
$.bm=!0
try{if(H.a7(a,b))return a
u=H.be(b)
t=H.y(a,u)
throw H.c(t)}finally{$.bm=!1}},
S:function(a,b){if(a!=null&&!H.bq(a,b))H.W(H.y(a,H.be(b)))
return a},
y:function(a,b){return new H.aA("TypeError: "+P.aj(a)+": type '"+H.a(H.cw(a))+"' is not a subtype of type '"+b+"'")},
cw:function(a){var u,t=J.p(a)
if(!!t.$iK){u=H.bR(t)
if(u!=null)return H.be(u)
return"Closure"}return H.a0(a)},
cz:function(a){throw H.c(new H.aE(a))},
cU:function(a){throw H.c(new P.ah(a))},
bS:function(a){return v.getIsolateTag(a)},
bv:function(a,b){a.$ti=b
return a},
T:function(a){if(a==null)return
return a.$ti},
dc:function(a,b,c){return H.aa(a["$a"+H.a(c)],H.T(b))},
n:function(a,b){var u=H.T(a)
return u==null?null:u[b]},
be:function(a){return H.z(a,null)},
z:function(a,b){var u,t
if(a==null)return"dynamic"
if(a===-1)return"void"
if(typeof a==="object"&&a!==null&&a.constructor===Array)return H.I(a[0].name)+H.bo(a,1,b)
if(typeof a=="function")return H.I(a.name)
if(a===-2)return"dynamic"
if(typeof a==="number"){H.U(a)
if(b==null||a<0||a>=b.length)return"unexpected-generic-index:"+a
u=b.length
t=u-a-1
if(t<0||t>=u)return H.bt(b,t)
return H.a(b[t])}if('func' in a)return H.co(a,b)
if('futureOr' in a)return"FutureOr<"+H.z("type" in a?a.type:null,b)+">"
return"unknown-reified-type"},
co:function(a,a0){var u,t,s,r,q,p,o,n,m,l,k,j,i,h,g,f,e,d,c,b=", "
if("bounds" in a){u=a.bounds
if(a0==null){a0=H.bv([],[P.o])
t=null}else t=a0.length
s=a0.length
for(r=u.length,q=r;q>0;--q)C.e.B(a0,"T"+(s+q))
for(p="<",o="",q=0;q<r;++q,o=b){p+=o
n=a0.length
m=n-q-1
if(m<0)return H.bt(a0,m)
p=C.f.j(p,a0[m])
l=u[q]
if(l!=null&&l!==P.d)p+=" extends "+H.z(l,a0)}p+=">"}else{p=""
t=null}k=!!a.v?"void":H.z(a.ret,a0)
if("args" in a){j=a.args
for(n=j.length,i="",h="",g=0;g<n;++g,h=b){f=j[g]
i=i+h+H.z(f,a0)}}else{i=""
h=""}if("opt" in a){e=a.opt
i+=h+"["
for(n=e.length,h="",g=0;g<n;++g,h=b){f=e[g]
i=i+h+H.z(f,a0)}i+="]"}if("named" in a){d=a.named
i+=h+"{"
for(n=H.cE(d),m=n.length,h="",g=0;g<m;++g,h=b){c=H.A(n[g])
i=i+h+H.z(d[c],a0)+(" "+H.a(c))}i+="}"}if(t!=null)a0.length=t
return p+"("+i+") => "+k},
bo:function(a,b,c){var u,t,s,r,q,p
if(a==null)return""
u=new P.a3("")
for(t=b,s="",r=!0,q="";t<a.length;++t,s=", "){u.a=q+s
p=a[t]
if(p!=null)r=!1
q=u.a+=H.z(p,c)}return"<"+u.h(0)+">"},
aa:function(a,b){if(a==null)return b
a=a.apply(null,b)
if(a==null)return
if(typeof a==="object"&&a!==null&&a.constructor===Array)return a
if(typeof a=="function")return a.apply(null,b)
return b},
a6:function(a,b,c,d){var u,t
if(a==null)return!1
u=H.T(a)
t=J.p(a)
if(t[b]==null)return!1
return H.bO(H.aa(t[d],u),null,c,null)},
cy:function(a,b,c,d){if(a==null)return a
if(H.a6(a,b,c,d))return a
throw H.c(H.y(a,function(e,f){return e.replace(/[^<,> ]+/g,function(g){return f[g]||g})}(H.I(b.substring(2))+H.bo(c,0,null),v.mangledGlobalNames)))},
bO:function(a,b,c,d){var u,t
if(c==null)return!0
if(a==null){u=c.length
for(t=0;t<u;++t)if(!H.m(null,null,c[t],d))return!1
return!0}u=a.length
for(t=0;t<u;++t)if(!H.m(a[t],b,c[t],d))return!1
return!0},
db:function(a,b,c){return a.apply(b,H.aa(J.p(b)["$a"+H.a(c)],H.T(b)))},
bU:function(a){var u
if(typeof a==="number")return!1
if('futureOr' in a){u="type" in a?a.type:null
return a==null||a.name==="d"||a.name==="i"||a===-1||a===-2||H.bU(u)}return!1},
bq:function(a,b){var u,t
if(a==null)return b==null||b.name==="d"||b.name==="i"||b===-1||b===-2||H.bU(b)
if(b==null||b===-1||b.name==="d"||b===-2)return!0
if(typeof b=="object"){if('futureOr' in b)if(H.bq(a,"type" in b?b.type:null))return!0
if('func' in b)return H.a7(a,b)}u=J.p(a).constructor
t=H.T(a)
if(t!=null){t=t.slice()
t.splice(0,0,u)
u=t}return H.m(u,null,b,null)},
v:function(a,b){if(a!=null&&!H.bq(a,b))throw H.c(H.y(a,H.be(b)))
return a},
m:function(a,b,c,d){var u,t,s,r,q,p,o,n,m,l=null
if(a===c)return!0
if(c==null||c===-1||c.name==="d"||c===-2)return!0
if(a===-2)return!0
if(a==null||a===-1||a.name==="d"||a===-2){if(typeof c==="number")return!1
if('futureOr' in c)return H.m(a,b,"type" in c?c.type:l,d)
return!1}if(typeof a==="number")return H.m(b[H.U(a)],b,c,d)
if(typeof c==="number")return!1
if(a.name==="i")return!0
u=typeof a==="object"&&a!==null&&a.constructor===Array
t=u?a[0]:a
if('futureOr' in c){s="type" in c?c.type:l
if('futureOr' in a)return H.m("type" in a?a.type:l,b,s,d)
else if(H.m(a,b,s,d))return!0
else{if(!('$i'+"r" in t.prototype))return!1
r=t.prototype["$a"+"r"]
q=H.aa(r,u?a.slice(1):l)
return H.m(typeof q==="object"&&q!==null&&q.constructor===Array?q[0]:l,b,s,d)}}if('func' in c)return H.bK(a,b,c,d)
if('func' in a)return c.name==="bh"
p=typeof c==="object"&&c!==null&&c.constructor===Array
o=p?c[0]:c
if(o!==t){n=o.name
if(!('$i'+n in t.prototype))return!1
m=t.prototype["$a"+n]}else m=l
if(!p)return!0
u=u?a.slice(1):l
p=c.slice(1)
return H.bO(H.aa(m,u),b,p,d)},
bK:function(a,b,c,d){var u,t,s,r,q,p,o,n,m,l,k,j,i,h,g
if(!('func' in a))return!1
if("bounds" in a){if(!("bounds" in c))return!1
u=a.bounds
t=c.bounds
if(u.length!==t.length)return!1
b=b==null?u:u.concat(b)
d=d==null?t:t.concat(d)}else if("bounds" in c)return!1
if(!H.m(a.ret,b,c.ret,d))return!1
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
for(k=0;k<o;++k)if(!H.m(r[k],d,s[k],b))return!1
for(j=k,i=0;j<n;++i,++j)if(!H.m(r[j],d,q[i],b))return!1
for(j=0;j<l;++i,++j)if(!H.m(p[j],d,q[i],b))return!1
h=a.named
g=c.named
if(g==null)return!0
if(h==null)return!1
return H.cO(h,b,g,d)},
cO:function(a,b,c,d){var u,t,s,r=Object.getOwnPropertyNames(c)
for(u=r.length,t=0;t<u;++t){s=r[t]
if(!Object.hasOwnProperty.call(a,s))return!1
if(!H.m(c[s],d,a[s],b))return!1}return!0},
cM:function(a){var u,t,s,r,q=H.A($.bT.$1(a)),p=$.b5[q]
if(p!=null){Object.defineProperty(a,v.dispatchPropertyName,{value:p,enumerable:false,writable:true,configurable:true})
return p.i}u=$.ba[q]
if(u!=null)return u
t=v.interceptorsByTag[q]
if(t==null){q=H.A($.bN.$2(a,q))
if(q!=null){p=$.b5[q]
if(p!=null){Object.defineProperty(a,v.dispatchPropertyName,{value:p,enumerable:false,writable:true,configurable:true})
return p.i}u=$.ba[q]
if(u!=null)return u
t=v.interceptorsByTag[q]}}if(t==null)return
u=t.prototype
s=q[0]
if(s==="!"){p=H.bb(u)
$.b5[q]=p
Object.defineProperty(a,v.dispatchPropertyName,{value:p,enumerable:false,writable:true,configurable:true})
return p.i}if(s==="~"){$.ba[q]=u
return u}if(s==="-"){r=H.bb(u)
Object.defineProperty(Object.getPrototypeOf(a),v.dispatchPropertyName,{value:r,enumerable:false,writable:true,configurable:true})
return r.i}if(s==="+")return H.bW(a,u)
if(s==="*")throw H.c(P.bH(q))
if(v.leafTags[q]===true){r=H.bb(u)
Object.defineProperty(Object.getPrototypeOf(a),v.dispatchPropertyName,{value:r,enumerable:false,writable:true,configurable:true})
return r.i}else return H.bW(a,u)},
bW:function(a,b){var u=Object.getPrototypeOf(a)
Object.defineProperty(u,v.dispatchPropertyName,{value:J.bu(b,u,null,null),enumerable:false,writable:true,configurable:true})
return b},
bb:function(a){return J.bu(a,!1,null,!!a.$icY)},
cN:function(a,b,c){var u=b.prototype
if(v.leafTags[a]===true)return H.bb(u)
else return J.bu(u,c,null,null)},
cJ:function(){if(!0===$.bs)return
$.bs=!0
H.cK()},
cK:function(){var u,t,s,r,q,p,o,n
$.b5=Object.create(null)
$.ba=Object.create(null)
H.cI()
u=v.interceptorsByTag
t=Object.getOwnPropertyNames(u)
if(typeof window!="undefined"){window
s=function(){}
for(r=0;r<t.length;++r){q=t[r]
p=$.bX.$1(q)
if(p!=null){o=H.cN(q,u[q],p)
if(o!=null){Object.defineProperty(p,v.dispatchPropertyName,{value:o,enumerable:false,writable:true,configurable:true})
s.prototype=p}}}}for(r=0;r<t.length;++r){q=t[r]
if(/^[A-Za-z_]/.test(q)){n=u[q]
u["!"+q]=n
u["~"+q]=n
u["-"+q]=n
u["+"+q]=n
u["*"+q]=n}}},
cI:function(){var u,t,s,r,q,p,o=C.i()
o=H.G(C.j,H.G(C.k,H.G(C.d,H.G(C.d,H.G(C.l,H.G(C.m,H.G(C.n(C.c),o)))))))
if(typeof dartNativeDispatchHooksTransformer!="undefined"){u=dartNativeDispatchHooksTransformer
if(typeof u=="function")u=[u]
if(u.constructor==Array)for(t=0;t<u.length;++t){s=u[t]
if(typeof s=="function")o=s(o)||o}}r=o.getTag
q=o.getUnknownTag
p=o.prototypeForTag
$.bT=new H.b7(r)
$.bN=new H.b8(q)
$.bX=new H.b9(p)},
G:function(a,b){return a(b)||b},
cR:function(a){if(/[[\]{}()*+?.\\^$|]/.test(a))return a.replace(/[[\]{}()*+?.\\^$|]/g,"\\$&")
return a},
ay:function ay(a,b,c,d,e,f){var _=this
_.a=a
_.b=b
_.c=c
_.d=d
_.e=e
_.f=f},
ar:function ar(a,b){this.a=a
this.b=b},
ap:function ap(a,b,c){this.a=a
this.b=b
this.c=c},
aC:function aC(a){this.a=a},
bf:function bf(a){this.a=a},
a5:function a5(a){this.a=a
this.b=null},
K:function K(){},
ax:function ax(){},
aw:function aw(){},
X:function X(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.d=d},
aA:function aA(a){this.a=a},
au:function au(a){this.a=a},
aE:function aE(a){this.a=a},
b7:function b7(a){this.a=a},
b8:function b8(a){this.a=a},
b9:function b9(a){this.a=a},
cE:function(a){return J.bD(H.bv(a?Object.keys(a):[],[null]))},
cV:function(a){return v.mangledGlobalNames[a]}},J={
bu:function(a,b,c,d){return{i:a,p:b,e:c,x:d}},
cG:function(a){var u,t,s,r,q=a[v.dispatchPropertyName]
if(q==null)if($.bs==null){H.cJ()
q=a[v.dispatchPropertyName]}if(q!=null){u=q.p
if(!1===u)return q.i
if(!0===u)return a
t=Object.getPrototypeOf(a)
if(u===t)return q.i
if(q.e===t)throw H.c(P.bH("Return interceptor for "+H.a(u(a,q))))}s=a.constructor
r=s==null?null:s[$.bw()]
if(r!=null)return r
r=H.cM(a)
if(r!=null)return r
if(typeof a=="function")return C.q
u=Object.getPrototypeOf(a)
if(u==null)return C.h
if(u===Object.prototype)return C.h
if(typeof s=="function"){Object.defineProperty(s,$.bw(),{value:C.b,enumerable:false,writable:true,configurable:true})
return C.b}return C.b},
bD:function(a){a.fixed$length=Array
return a},
p:function(a){if(typeof a=="number"){if(Math.floor(a)==a)return J.Y.prototype
return J.am.prototype}if(typeof a=="string")return J.L.prototype
if(a==null)return J.an.prototype
if(typeof a=="boolean")return J.al.prototype
if(a.constructor==Array)return J.C.prototype
if(typeof a!="object"){if(typeof a=="function")return J.Z.prototype
return a}if(a instanceof P.d)return a
return J.cG(a)},
cF:function(a){if(typeof a=="string")return J.L.prototype
if(a==null)return a
if(a.constructor==Array)return J.C.prototype
if(!(a instanceof P.d))return J.N.prototype
return a},
by:function(a){return J.cF(a).gm(a)},
ac:function(a){return J.p(a).h(a)},
h:function h(){},
al:function al(){},
an:function an(){},
a_:function a_(){},
as:function as(){},
N:function N(){},
Z:function Z(){},
C:function C(a){this.$ti=a},
bi:function bi(a){this.$ti=a},
ad:function ad(a,b,c){var _=this
_.a=a
_.b=b
_.c=0
_.d=null
_.$ti=c},
ao:function ao(){},
Y:function Y(){},
am:function am(){},
L:function L(){}},P={
cj:function(){var u,t,s={}
if(self.scheduleImmediate!=null)return P.cA()
if(self.MutationObserver!=null&&self.document!=null){u=self.document.createElement("div")
t=self.document.createElement("span")
s.a=null
new self.MutationObserver(H.R(new P.aH(s),1)).observe(u,{childList:true})
return new P.aG(s,u,t)}else if(self.setImmediate!=null)return P.cB()
return P.cC()},
ck:function(a){self.scheduleImmediate(H.R(new P.aI(H.b(a,{func:1,ret:-1})),0))},
cl:function(a){self.setImmediate(H.R(new P.aJ(H.b(a,{func:1,ret:-1})),0))},
cm:function(a){H.b(a,{func:1,ret:-1})
P.cn(0,a)},
cn:function(a,b){var u=new P.b1()
u.G(a,b)
return u},
bJ:function(a,b){var u,t,s
b.a=1
try{a.E(new P.aQ(b),new P.aR(b),P.i)}catch(s){u=H.ab(s)
t=H.a8(s)
P.cS(new P.aS(b,u,t))}},
aP:function(a,b){var u,t
for(;u=a.a,u===2;)a=H.e(a.c,"$il")
if(u>=4){t=b.k()
b.a=a.a
b.c=a.c
P.D(b,t)}else{t=H.e(b.c,"$iu")
b.a=2
b.c=a
a.A(t)}},
D:function(a,b){var u,t,s,r,q,p,o,n,m,l,k,j,i=null,h={},g=h.a=a
for(;!0;){u={}
t=g.a===8
if(b==null){if(t){s=H.e(g.c,"$ij")
P.bp(i,i,g.b,s.a,s.b)}return}for(;r=b.a,r!=null;b=r){b.a=null
P.D(h.a,b)}g=h.a
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
if(m){H.e(q,"$ij")
P.bp(i,i,g.b,q.a,q.b)
return}l=$.f
if(l!==n)$.f=n
else l=i
g=b.c
if((g&15)===8)new P.aX(h,u,b,t).$0()
else if(p){if((g&1)!==0)new P.aW(u,b,q).$0()}else if((g&2)!==0)new P.aV(h,u,b).$0()
if(l!=null)$.f=l
g=u.b
if(!!J.p(g).$ir){if(g.a>=4){k=H.e(o.c,"$iu")
o.c=null
b=o.l(k)
o.a=g.a
o.c=g.c
h.a=g
continue}else P.aP(g,o)
return}}j=b.b
k=H.e(j.c,"$iu")
j.c=null
b=j.l(k)
g=u.a
p=u.b
if(!g){H.v(p,H.n(j,0))
j.a=4
j.c=p}else{H.e(p,"$ij")
j.a=8
j.c=p}h.a=j
g=j}},
cr:function(a,b){if(H.a7(a,{func:1,args:[P.d,P.k]}))return H.b(a,{func:1,ret:null,args:[P.d,P.k]})
if(H.a7(a,{func:1,args:[P.d]}))return H.b(a,{func:1,ret:null,args:[P.d]})
throw H.c(P.bz(a,"onError","Error handler must accept one Object or one Object and a StackTrace as arguments, and return a a valid result"))},
cq:function(){var u,t
for(;u=$.E,u!=null;){$.P=null
t=u.b
$.E=t
if(t==null)$.O=null
u.a.$0()}},
cv:function(){$.bn=!0
try{P.cq()}finally{$.P=null
$.bn=!1
if($.E!=null)$.bx().$1(P.bP())}},
bM:function(a){var u=new P.a4(a)
if($.E==null){$.E=$.O=u
if(!$.bn)$.bx().$1(P.bP())}else $.O=$.O.b=u},
cu:function(a){var u,t,s=$.E
if(s==null){P.bM(a)
$.P=$.O
return}u=new P.a4(a)
t=$.P
if(t==null){u.b=s
$.E=$.P=u}else{u.b=t.b
$.P=t.b=u
if(u.b==null)$.O=u}},
cS:function(a){var u=null,t=$.f
if(C.a===t){P.F(u,u,C.a,a)
return}P.F(u,u,t,H.b(t.C(a),{func:1,ret:-1}))},
bp:function(a,b,c,d,e){var u={}
u.a=d
P.cu(new P.b4(u,e))},
bL:function(a,b,c,d,e){var u,t=$.f
if(t===c)return d.$0()
$.f=c
u=t
try{t=d.$0()
return t}finally{$.f=u}},
ct:function(a,b,c,d,e,f,g){var u,t=$.f
if(t===c)return d.$1(e)
$.f=c
u=t
try{t=d.$1(e)
return t}finally{$.f=u}},
cs:function(a,b,c,d,e,f,g,h,i){var u,t=$.f
if(t===c)return d.$2(e,f)
$.f=c
u=t
try{t=d.$2(e,f)
return t}finally{$.f=u}},
F:function(a,b,c,d){var u
H.b(d,{func:1,ret:-1})
u=C.a!==c
if(u)d=!(!u||!1)?c.C(d):c.N(d,-1)
P.bM(d)},
aH:function aH(a){this.a=a},
aG:function aG(a,b,c){this.a=a
this.b=b
this.c=c},
aI:function aI(a){this.a=a},
aJ:function aJ(a){this.a=a},
b1:function b1(){},
b2:function b2(a,b){this.a=a
this.b=b},
aK:function aK(){},
aF:function aF(a,b){this.a=a
this.$ti=b},
u:function u(a,b,c,d,e){var _=this
_.a=null
_.b=a
_.c=b
_.d=c
_.e=d
_.$ti=e},
l:function l(a,b){var _=this
_.a=0
_.b=a
_.c=null
_.$ti=b},
aM:function aM(a,b){this.a=a
this.b=b},
aU:function aU(a,b){this.a=a
this.b=b},
aQ:function aQ(a){this.a=a},
aR:function aR(a){this.a=a},
aS:function aS(a,b,c){this.a=a
this.b=b
this.c=c},
aO:function aO(a,b){this.a=a
this.b=b},
aT:function aT(a,b){this.a=a
this.b=b},
aN:function aN(a,b,c){this.a=a
this.b=b
this.c=c},
aX:function aX(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.d=d},
aY:function aY(a){this.a=a},
aW:function aW(a,b,c){this.a=a
this.b=b
this.c=c},
aV:function aV(a,b,c){this.a=a
this.b=b
this.c=c},
a4:function a4(a){this.a=a
this.b=null},
j:function j(a,b){this.a=a
this.b=b},
b3:function b3(){},
b4:function b4(a,b){this.a=a
this.b=b},
aZ:function aZ(){},
b0:function b0(a,b,c){this.a=a
this.b=b
this.c=c},
b_:function b_(a,b){this.a=a
this.b=b},
ce:function(a){if(a instanceof H.K)return a.h(0)
return"Instance of '"+H.a(H.a0(a))+"'"},
ci:function(a,b,c){var u=new J.ad(b,b.length,[H.n(b,0)])
if(!u.t())return a
if(c.length===0){do a+=H.a(u.d)
while(u.t())}else{a+=H.a(u.d)
for(;u.t();)a=a+c+H.a(u.d)}return a},
aj:function(a){if(typeof a==="number"||typeof a==="boolean"||null==a)return J.ac(a)
if(typeof a==="string")return JSON.stringify(a)
return P.ce(a)},
bz:function(a,b,c){return new P.w(!0,a,b,c)},
bl:function(a,b){return new P.at(!0,a,b,"Value not in range")},
bI:function(a){return new P.aD(a)},
bH:function(a){return new P.aB(a)},
bF:function(a){return new P.av(a)},
H:function H(){},
b6:function b6(){},
B:function B(){},
ae:function ae(){},
M:function M(){},
w:function w(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.d=d},
at:function at(a,b,c,d){var _=this
_.a=a
_.b=b
_.c=c
_.d=d},
ak:function ak(a,b,c,d,e){var _=this
_.f=a
_.a=b
_.b=c
_.c=d
_.d=e},
aD:function aD(a){this.a=a},
aB:function aB(a){this.a=a},
av:function av(a){this.a=a},
ag:function ag(a){this.a=a},
a2:function a2(){},
ah:function ah(a){this.a=a},
aL:function aL(a){this.a=a},
a9:function a9(){},
aq:function aq(){},
i:function i(){},
V:function V(){},
d:function d(){},
k:function k(){},
o:function o(){},
a3:function a3(a){this.a=a},
cP:function(a,b){var u=new P.l($.f,[b]),t=new P.aF(u,[b])
a.then(H.R(new P.bc(t,b),1),H.R(new P.bd(t),1))
return u},
bc:function bc(a,b){this.a=a
this.b=b},
bd:function bd(a){this.a=a},
cg:function(a,b,c){var u,t
if(P.cp(a))return b+"..."+c
u=new P.a3(b)
C.e.B($.Q,a)
try{t=u
t.a=P.ci(t.a,a,", ")}finally{if(0>=$.Q.length)return H.bt($.Q,-1)
$.Q.pop()}u.a+=c
t=u.a
return t.charCodeAt(0)==0?t:t},
cp:function(a){var u,t
for(u=$.Q.length,t=0;t<u;++t)if(a===$.Q[t])return!0
return!1}},W={ai:function ai(){},x:function x(){},a1:function a1(){}},M={
bV:function(){var u=window.navigator.serviceWorker
P.cP(u.register("/sw.js",null),W.a1)}}
var w=[C,H,J,P,W,M]
hunkHelpers.setFunctionNamesIfNecessary(w)
var $={}
H.bj.prototype={}
J.h.prototype={
h:function(a){return"Instance of '"+H.a(H.a0(a))+"'"}}
J.al.prototype={
h:function(a){return String(a)},
$iH:1}
J.an.prototype={
h:function(a){return"null"},
$ii:1}
J.a_.prototype={
h:function(a){return String(a)}}
J.as.prototype={}
J.N.prototype={}
J.Z.prototype={
h:function(a){var u=a[$.bZ()]
if(u==null)return this.F(a)
return"JavaScript function for "+H.a(J.ac(u))},
$S:function(){return{func:1,opt:[,,,,,,,,,,,,,,,,]}},
$ibh:1}
J.C.prototype={
B:function(a,b){H.v(b,H.n(a,0))
if(!!a.fixed$length)H.W(P.bI("add"))
a.push(b)},
h:function(a){return P.cg(a,"[","]")},
gm:function(a){return a.length},
$icf:1}
J.bi.prototype={}
J.ad.prototype={
t:function(){var u,t=this,s=t.a,r=s.length
if(t.b!==r)throw H.c(H.cT(s))
u=t.c
if(u>=r){t.sw(null)
return!1}t.sw(s[u]);++t.c
return!0},
sw:function(a){this.d=H.v(a,H.n(this,0))}}
J.ao.prototype={
h:function(a){if(a===0&&1/a<0)return"-0.0"
else return""+a},
M:function(a,b){var u
if(a>0)u=this.L(a,b)
else{u=b>31?31:b
u=a>>u>>>0}return u},
L:function(a,b){return b>31?0:a>>>b},
$iV:1}
J.Y.prototype={$ia9:1}
J.am.prototype={}
J.L.prototype={
K:function(a,b){if(b>=a.length)throw H.c(H.bQ(a,b))
return a.charCodeAt(b)},
j:function(a,b){if(typeof b!=="string")throw H.c(P.bz(b,null,null))
return a+b},
h:function(a){return a},
gm:function(a){return a.length},
$io:1}
H.ay.prototype={
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
H.ar.prototype={
h:function(a){var u=this.b
if(u==null)return"NoSuchMethodError: "+H.a(this.a)
return"NoSuchMethodError: method not found: '"+u+"' on null"}}
H.ap.prototype={
h:function(a){var u,t=this,s="NoSuchMethodError: method not found: '",r=t.b
if(r==null)return"NoSuchMethodError: "+H.a(t.a)
u=t.c
if(u==null)return s+r+"' ("+H.a(t.a)+")"
return s+r+"' on '"+u+"' ("+H.a(t.a)+")"}}
H.aC.prototype={
h:function(a){var u=this.a
return u.length===0?"Error":"Error: "+u}}
H.bf.prototype={
$1:function(a){if(!!J.p(a).$iB)if(a.$thrownJsError==null)a.$thrownJsError=this.a
return a},
$S:3}
H.a5.prototype={
h:function(a){var u,t=this.b
if(t!=null)return t
t=this.a
u=t!==null&&typeof t==="object"?t.stack:null
return this.b=u==null?"":u},
$ik:1}
H.K.prototype={
h:function(a){var u=this.constructor,t=u==null?null:u.name
return"Closure '"+H.I(t==null?"unknown":t)+"'"},
$ibh:1,
gU:function(){return this},
$C:"$1",
$R:1,
$D:null}
H.ax.prototype={}
H.aw.prototype={
h:function(a){var u=this.$static_name
if(u==null)return"Closure of unknown static method"
return"Closure '"+H.I(u)+"'"}}
H.X.prototype={
h:function(a){var u=this.c
if(u==null)u=this.a
return"Closure '"+H.a(this.d)+"' of "+("Instance of '"+H.a(H.a0(u))+"'")}}
H.aA.prototype={
h:function(a){return this.a}}
H.au.prototype={
h:function(a){return"RuntimeError: "+this.a}}
H.aE.prototype={
h:function(a){return"Assertion failed: "+P.aj(this.a)}}
H.b7.prototype={
$1:function(a){return this.a(a)},
$S:3}
H.b8.prototype={
$2:function(a,b){return this.a(a,b)},
$S:6}
H.b9.prototype={
$1:function(a){return this.a(H.A(a))},
$S:7}
P.aH.prototype={
$1:function(a){var u=this.a,t=u.a
u.a=null
t.$0()},
$S:4}
P.aG.prototype={
$1:function(a){var u,t
this.a.a=H.b(a,{func:1,ret:-1})
u=this.b
t=this.c
u.firstChild?u.removeChild(t):u.appendChild(t)},
$S:8}
P.aI.prototype={
$0:function(){this.a.$0()},
$S:0}
P.aJ.prototype={
$0:function(){this.a.$0()},
$S:0}
P.b1.prototype={
G:function(a,b){if(self.setTimeout!=null)self.setTimeout(H.R(new P.b2(this,b),0),a)
else throw H.c(P.bI("`setTimeout()` not found."))}}
P.b2.prototype={
$0:function(){this.b.$0()},
$S:1}
P.aK.prototype={}
P.aF.prototype={}
P.u.prototype={
P:function(a){if((this.c&15)!==6)return!0
return this.b.b.u(H.b(this.d,{func:1,ret:P.H,args:[P.d]}),a.a,P.H,P.d)},
O:function(a){var u=this.e,t=P.d,s={futureOr:1,type:H.n(this,1)},r=this.b.b
if(H.a7(u,{func:1,args:[P.d,P.k]}))return H.S(r.R(u,a.a,a.b,null,t,P.k),s)
else return H.S(r.u(H.b(u,{func:1,args:[P.d]}),a.a,null,t),s)}}
P.l.prototype={
E:function(a,b,c){var u,t,s,r=H.n(this,0)
H.b(a,{func:1,ret:{futureOr:1,type:c},args:[r]})
u=$.f
if(u!==C.a){H.b(a,{func:1,ret:{futureOr:1,type:c},args:[r]})
if(b!=null)b=P.cr(b,u)}t=new P.l($.f,[c])
s=b==null?1:3
this.v(new P.u(t,s,a,b,[r,c]))
return t},
T:function(a,b){return this.E(a,null,b)},
v:function(a){var u,t=this,s=t.a
if(s<=1){a.a=H.e(t.c,"$iu")
t.c=a}else{if(s===2){u=H.e(t.c,"$il")
s=u.a
if(s<4){u.v(a)
return}t.a=s
t.c=u.c}P.F(null,null,t.b,H.b(new P.aM(t,a),{func:1,ret:-1}))}},
A:function(a){var u,t,s,r,q,p=this,o={}
o.a=a
if(a==null)return
u=p.a
if(u<=1){t=H.e(p.c,"$iu")
s=p.c=a
if(t!=null){for(;r=s.a,r!=null;s=r);s.a=t}}else{if(u===2){q=H.e(p.c,"$il")
u=q.a
if(u<4){q.A(a)
return}p.a=u
p.c=q.c}o.a=p.l(a)
P.F(null,null,p.b,H.b(new P.aU(o,p),{func:1,ret:-1}))}},
k:function(){var u=H.e(this.c,"$iu")
this.c=null
return this.l(u)},
l:function(a){var u,t,s
for(u=a,t=null;u!=null;t=u,u=s){s=u.a
u.a=t}return t},
n:function(a,b){var u,t=this
H.e(b,"$ik")
u=t.k()
t.a=8
t.c=new P.j(a,b)
P.D(t,u)},
H:function(a){var u=this
H.S(a,{futureOr:1,type:H.n(u,0)})
if(H.a6(a,"$ir",u.$ti,"$ar")){u.J(a)
return}u.a=1
P.F(null,null,u.b,H.b(new P.aO(u,a),{func:1,ret:-1}))},
J:function(a){var u=this,t=u.$ti
H.cy(a,"$ir",t,"$ar")
if(H.a6(a,"$il",t,null)){if(a.a===8){u.a=1
P.F(null,null,u.b,H.b(new P.aT(u,a),{func:1,ret:-1}))}else P.aP(a,u)
return}P.bJ(a,u)},
I:function(a,b){this.a=1
P.F(null,null,this.b,H.b(new P.aN(this,a,b),{func:1,ret:-1}))},
$ir:1}
P.aM.prototype={
$0:function(){P.D(this.a,this.b)},
$S:0}
P.aU.prototype={
$0:function(){P.D(this.b,this.a.a)},
$S:0}
P.aQ.prototype={
$1:function(a){var u,t,s=this.a
s.a=0
u=H.n(s,0)
H.S(a,{futureOr:1,type:u})
if(H.a6(a,"$ir",[u],"$ar"))if(H.a6(a,"$il",[u],null))P.aP(a,s)
else P.bJ(a,s)
else{t=s.k()
H.v(a,u)
s.a=4
s.c=a
P.D(s,t)}},
$S:4}
P.aR.prototype={
$2:function(a,b){H.e(b,"$ik")
this.a.n(a,b)},
$1:function(a){return this.$2(a,null)},
$S:9}
P.aS.prototype={
$0:function(){this.a.n(this.b,this.c)},
$S:0}
P.aO.prototype={
$0:function(){var u=this.a,t=H.v(this.b,H.n(u,0)),s=u.k()
u.a=4
u.c=t
P.D(u,s)},
$S:0}
P.aT.prototype={
$0:function(){P.aP(this.b,this.a)},
$S:0}
P.aN.prototype={
$0:function(){this.a.n(this.b,this.c)},
$S:0}
P.aX.prototype={
$0:function(){var u,t,s,r,q,p,o=this,n=null
try{s=o.c
n=s.b.b.D(H.b(s.d,{func:1}),null)}catch(r){u=H.ab(r)
t=H.a8(r)
if(o.d){s=H.e(o.a.a.c,"$ij").a
q=u
q=s==null?q==null:s===q
s=q}else s=!1
q=o.b
if(s)q.b=H.e(o.a.a.c,"$ij")
else q.b=new P.j(u,t)
q.a=!0
return}if(!!J.p(n).$ir){if(n instanceof P.l&&n.a>=4){if(n.a===8){s=o.b
s.b=H.e(n.c,"$ij")
s.a=!0}return}p=o.a.a
s=o.b
s.b=n.T(new P.aY(p),null)
s.a=!1}},
$S:1}
P.aY.prototype={
$1:function(a){return this.a},
$S:10}
P.aW.prototype={
$0:function(){var u,t,s,r,q,p,o,n=this
try{s=n.b
r=H.n(s,0)
q=H.v(n.c,r)
p=H.n(s,1)
n.a.b=s.b.b.u(H.b(s.d,{func:1,ret:{futureOr:1,type:p},args:[r]}),q,{futureOr:1,type:p},r)}catch(o){u=H.ab(o)
t=H.a8(o)
s=n.a
s.b=new P.j(u,t)
s.a=!0}},
$S:1}
P.aV.prototype={
$0:function(){var u,t,s,r,q,p,o,n,m=this
try{u=H.e(m.a.a.c,"$ij")
r=m.c
if(H.cD(r.P(u))&&r.e!=null){q=m.b
q.b=r.O(u)
q.a=!1}}catch(p){t=H.ab(p)
s=H.a8(p)
r=H.e(m.a.a.c,"$ij")
q=r.a
o=t
n=m.b
if(q==null?o==null:q===o)n.b=r
else n.b=new P.j(t,s)
n.a=!0}},
$S:1}
P.a4.prototype={}
P.j.prototype={
h:function(a){return H.a(this.a)},
$iB:1}
P.b3.prototype={$id8:1}
P.b4.prototype={
$0:function(){var u,t=this.a,s=t.a
t=s==null?t.a=new P.M():s
s=this.b
if(s==null)throw H.c(t)
u=H.c(t)
u.stack=s.h(0)
throw u},
$S:0}
P.aZ.prototype={
S:function(a){var u,t,s,r=null
H.b(a,{func:1,ret:-1})
try{if(C.a===$.f){a.$0()
return}P.bL(r,r,this,a,-1)}catch(s){u=H.ab(s)
t=H.a8(s)
P.bp(r,r,this,u,H.e(t,"$ik"))}},
N:function(a,b){return new P.b0(this,H.b(a,{func:1,ret:b}),b)},
C:function(a){return new P.b_(this,H.b(a,{func:1,ret:-1}))},
D:function(a,b){H.b(a,{func:1,ret:b})
if($.f===C.a)return a.$0()
return P.bL(null,null,this,a,b)},
u:function(a,b,c,d){H.b(a,{func:1,ret:c,args:[d]})
H.v(b,d)
if($.f===C.a)return a.$1(b)
return P.ct(null,null,this,a,b,c,d)},
R:function(a,b,c,d,e,f){H.b(a,{func:1,ret:d,args:[e,f]})
H.v(b,e)
H.v(c,f)
if($.f===C.a)return a.$2(b,c)
return P.cs(null,null,this,a,b,c,d,e,f)}}
P.b0.prototype={
$0:function(){return this.a.D(this.b,this.c)},
$S:function(){return{func:1,ret:this.c}}}
P.b_.prototype={
$0:function(){return this.a.S(this.b)},
$S:1}
P.H.prototype={}
P.b6.prototype={}
P.B.prototype={}
P.ae.prototype={
h:function(a){return"Assertion failed"}}
P.M.prototype={
h:function(a){return"Throw of null."}}
P.w.prototype={
gq:function(){return"Invalid argument"+(!this.a?"(s)":"")},
gp:function(){return""},
h:function(a){var u,t,s,r,q=this,p=q.c,o=p!=null?" ("+p+")":""
p=q.d
u=p==null?"":": "+p
t=q.gq()+o+u
if(!q.a)return t
s=q.gp()
r=P.aj(q.b)
return t+s+": "+r}}
P.at.prototype={
gq:function(){return"RangeError"},
gp:function(){return""}}
P.ak.prototype={
gq:function(){return"RangeError"},
gp:function(){var u,t=H.U(this.b)
if(typeof t!=="number")return t.V()
if(t<0)return": index must not be negative"
u=this.f
if(u===0)return": no indices are valid"
return": index should be less than "+u},
gm:function(a){return this.f}}
P.aD.prototype={
h:function(a){return"Unsupported operation: "+this.a}}
P.aB.prototype={
h:function(a){var u=this.a
return u!=null?"UnimplementedError: "+u:"UnimplementedError"}}
P.av.prototype={
h:function(a){return"Bad state: "+this.a}}
P.ag.prototype={
h:function(a){var u=this.a
if(u==null)return"Concurrent modification during iteration."
return"Concurrent modification during iteration: "+P.aj(u)+"."}}
P.a2.prototype={
h:function(a){return"Stack Overflow"},
$iB:1}
P.ah.prototype={
h:function(a){var u=this.a
return u==null?"Reading static variable during its initialization":"Reading static variable '"+u+"' during its initialization"}}
P.aL.prototype={
h:function(a){return"Exception: "+this.a}}
P.a9.prototype={}
P.aq.prototype={$icf:1}
P.i.prototype={
h:function(a){return"null"}}
P.V.prototype={}
P.d.prototype={constructor:P.d,$id:1,
h:function(a){return"Instance of '"+H.a(H.a0(this))+"'"},
toString:function(){return this.h(this)}}
P.k.prototype={}
P.o.prototype={}
P.a3.prototype={
gm:function(a){return this.a.length},
h:function(a){var u=this.a
return u.charCodeAt(0)==0?u:u}}
W.ai.prototype={
h:function(a){return String(a)}}
W.x.prototype={}
W.a1.prototype={$ia1:1}
P.bc.prototype={
$1:function(a){var u=this.a
a=H.S(H.S(a,{futureOr:1,type:this.b}),{futureOr:1,type:H.n(u,0)})
u=u.a
if(u.a!==0)H.W(P.bF("Future already completed"))
u.H(a)
return},
$S:5}
P.bd.prototype={
$1:function(a){var u=a==null?new P.M():a,t=this.a.a
if(t.a!==0)H.W(P.bF("Future already completed"))
t.I(u,null)
return},
$S:5};(function aliases(){var u=J.a_.prototype
u.F=u.h})();(function installTearOffs(){var u=hunkHelpers._static_1,t=hunkHelpers._static_0
u(P,"cA","ck",2)
u(P,"cB","cl",2)
u(P,"cC","cm",2)
t(P,"bP","cv",1)})();(function inheritance(){var u=hunkHelpers.inherit,t=hunkHelpers.inheritMany
u(P.d,null)
t(P.d,[H.bj,J.h,J.ad,H.ay,P.B,H.K,H.a5,P.b1,P.aK,P.u,P.l,P.a4,P.j,P.b3,P.H,P.V,P.a2,P.aL,P.aq,P.i,P.k,P.o,P.a3])
t(J.h,[J.al,J.an,J.a_,J.C,J.ao,J.L,W.ai,W.x])
t(J.a_,[J.as,J.N,J.Z])
u(J.bi,J.C)
t(J.ao,[J.Y,J.am])
t(P.B,[H.ar,H.ap,H.aC,H.aA,H.au,P.ae,P.M,P.w,P.aD,P.aB,P.av,P.ag,P.ah])
t(H.K,[H.bf,H.ax,H.b7,H.b8,H.b9,P.aH,P.aG,P.aI,P.aJ,P.b2,P.aM,P.aU,P.aQ,P.aR,P.aS,P.aO,P.aT,P.aN,P.aX,P.aY,P.aW,P.aV,P.b4,P.b0,P.b_,P.bc,P.bd])
t(H.ax,[H.aw,H.X])
u(H.aE,P.ae)
u(P.aF,P.aK)
u(P.aZ,P.b3)
t(P.V,[P.b6,P.a9])
t(P.w,[P.at,P.ak])
u(W.a1,W.x)})()
var v={mangledGlobalNames:{a9:"int",b6:"double",V:"num",o:"String",H:"bool",i:"Null",aq:"List"},mangledNames:{},getTypeFromName:getGlobalFromName,metadata:[],types:[{func:1,ret:P.i},{func:1,ret:-1},{func:1,ret:-1,args:[{func:1,ret:-1}]},{func:1,args:[,]},{func:1,ret:P.i,args:[,]},{func:1,ret:-1,args:[,]},{func:1,args:[,P.o]},{func:1,args:[P.o]},{func:1,ret:P.i,args:[{func:1,ret:-1}]},{func:1,ret:P.i,args:[,],opt:[P.k]},{func:1,ret:[P.l,,],args:[,]}],interceptorsByTag:null,leafTags:null};(function constants(){C.o=J.h.prototype
C.e=J.C.prototype
C.p=J.Y.prototype
C.f=J.L.prototype
C.q=J.Z.prototype
C.h=J.as.prototype
C.b=J.N.prototype
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

C.a=new P.aZ()})();(function staticFields(){$.q=0
$.J=null
$.bA=null
$.bm=!1
$.bT=null
$.bN=null
$.bX=null
$.b5=null
$.ba=null
$.bs=null
$.E=null
$.O=null
$.P=null
$.bn=!1
$.f=C.a
$.Q=[]})();(function lazyInitializers(){var u=hunkHelpers.lazy
u($,"cW","bZ",function(){return H.bS("_$dart_dartClosure")})
u($,"cX","bw",function(){return H.bS("_$dart_js")})
u($,"cZ","c_",function(){return H.t(H.az({
toString:function(){return"$receiver$"}}))})
u($,"d_","c0",function(){return H.t(H.az({$method$:null,
toString:function(){return"$receiver$"}}))})
u($,"d0","c1",function(){return H.t(H.az(null))})
u($,"d1","c2",function(){return H.t(function(){var $argumentsExpr$='$arguments$'
try{null.$method$($argumentsExpr$)}catch(t){return t.message}}())})
u($,"d4","c5",function(){return H.t(H.az(void 0))})
u($,"d5","c6",function(){return H.t(function(){var $argumentsExpr$='$arguments$'
try{(void 0).$method$($argumentsExpr$)}catch(t){return t.message}}())})
u($,"d3","c4",function(){return H.t(H.bG(null))})
u($,"d2","c3",function(){return H.t(function(){try{null.$method$}catch(t){return t.message}}())})
u($,"d7","c8",function(){return H.t(H.bG(void 0))})
u($,"d6","c7",function(){return H.t(function(){try{(void 0).$method$}catch(t){return t.message}}())})
u($,"d9","bx",function(){return P.cj()})})();(function nativeSupport(){!function(){var u=function(a){var o={}
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
hunkHelpers.setOrUpdateInterceptorsByTag({ApplicationCacheErrorEvent:J.h,DOMError:J.h,ErrorEvent:J.h,Event:J.h,InputEvent:J.h,MediaError:J.h,Navigator:J.h,NavigatorConcurrentHardware:J.h,NavigatorUserMediaError:J.h,OverconstrainedError:J.h,PositionError:J.h,SensorErrorEvent:J.h,SpeechRecognitionError:J.h,SQLError:J.h,DOMException:W.ai,EventTarget:W.x,ServiceWorkerContainer:W.x,Window:W.x,DOMWindow:W.x})
hunkHelpers.setOrUpdateLeafTags({ApplicationCacheErrorEvent:true,DOMError:true,ErrorEvent:true,Event:true,InputEvent:true,MediaError:true,Navigator:true,NavigatorConcurrentHardware:true,NavigatorUserMediaError:true,OverconstrainedError:true,PositionError:true,SensorErrorEvent:true,SpeechRecognitionError:true,SQLError:true,DOMException:true,EventTarget:true,ServiceWorkerContainer:true,Window:true,DOMWindow:true})})()
convertAllToFastObject(w)
convertToFastObject($);(function(a){if(typeof document==="undefined"){a(null)
return}if(typeof document.currentScript!='undefined'){a(document.currentScript)
return}var u=document.scripts
function onLoad(b){for(var s=0;s<u.length;++s)u[s].removeEventListener("load",onLoad,false)
a(b.target)}for(var t=0;t<u.length;++t)u[t].addEventListener("load",onLoad,false)})(function(a){v.currentScript=a
if(typeof dartMainRunner==="function")dartMainRunner(M.bV,[])
else M.bV([])})})()
//# sourceMappingURL=devices.dart.js.map
