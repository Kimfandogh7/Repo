const {getEncoding}=require('js-tiktoken');
const enc=getEncoding('cl100k_base');
let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{
  process.stdout.write(String(enc.encode(d).length));
});
