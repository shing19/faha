<template>
  <div class="all">
    <div class="background">
      <div id="loadingdisplay">Loading...</div>
      <div id="container" class="loading">
        <canvas id="glcanvas" width="100vw" height="100vh"></canvas>
      </div>
    </div>
    <section class="chat-box">
      <div class="chat-box-list-container" ref="chatbox">
        <ul class="chat-box-list">
          <li 
            class="message"
            v-for="(message, idx) in messages"
            :key="idx"
            :class="message.author"
          >
            <div v-show="(message.image==null)">
              <span v-show="!(message.text==null)">{{ message.text }}</span>
            </div>
            <img :id="idx" :src="message.image" v-show="!(message.image==null)" alt="image" style="width:65%" @load="scroll"/>
          </li>
        </ul> 
      </div>
      <div class="input">
        <label class="upload_cover">
          <input class="file" name="file" type="file" accept="image/png,image/gif,image/jpeg" @change="upload"/>
          <span class="upload_icon">➕</span>
        </label>
        <div class="chat-inputs">
          <input 
            type="text" 
            v-model="message" 
            @keyup.enter="sendMessage"
          />
          <button class="bn632-hover bn20" @click="sendMessage">SEND</button>
        </div>
      </div>
      <button class="bn6 restart" v-on:click="restart">RESTART</button>
    </section>
    <section class="img-box">
      <div class="img-box-list-container" ref="imgbox">
        <ul class="img-box-list">
          <li 
            class="img"
            v-for="(message, idx) in messages"
            :key="idx"
          >
            <img :id="idx" :src="message.image" v-show="!(message.image==null)" alt="image" style="width: 100%" @load="scroll"/>
          </li>
        </ul> 
      </div>
      <p class="display">{{ display }}</p>
    </section>
  </div>
</template>

<script>
import {L2Dwidget} from 'live2d-widget'
export default {
  name: 'ChatBox',
  data: () => ({
    message: '',
    text: '',
    messages: [],
    sender_id: '',
    filename: '',
    display: 'DISPLAY'
  }),
  mounted() {
      this.sender_id = uuidv4()
      console.log('generate sender id: '+this.sender_id)

      function uuidv4() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8)
            return v.toString(16)
        })
      }
      // background
      let script = document.createElement('script')
      script .setAttribute('src', 'static/js/patch.js')
      this.$el.appendChild(script);
      document.addEventListener('CABLES.jsLoaded',  event => {
        console.log('cables loaded')
        setTimeout(() =>{ this.init() },1500);
      })
		},
  methods: {
    sendMessage() {
      if (this.message != '') {
        this.text = this.message
        this.message = ''
        this.messages.push({
          text: this.text,
          author: 'client'
        })
        console.log('client says: ')
        console.log(this.text)
        this.$nextTick(() => {
          this.$refs.chatbox.scrollTop = this.$refs.chatbox.scrollHeight
          this.$refs.imgbox.scrollTop = this.$refs.imgbox.scrollHeight
        })
        this.$axios.post('http://1.117.208.226:5005/webhooks/rest/webhook', {
        // this.$axios.post('http://1.116.3.150:5005/webhooks/rest/webhook', {
        // this.$axios.post('http://localhost:5005/webhooks/rest/webhook', {
          "message": this.text,
          "sender": this.sender_id
        }, {timeout: 1000 * 60 * 4})
        .then(res => {
          // split starts here
          let msgtext = res.data[0].text
          console.log('text: ' + msgtext)
          if ( msgtext.search('//image//') != -1 ) {
            this.messages.push({
              text: msgtext.split('//image//')[0],
              // image: msgtext.split('//image//')[1],
              // image: res.data[0].image,
              author: 'server'
            })
            this.messages.push({
              // text: msgtext.split('//image//')[0],
              image: msgtext.split('//image//')[1],
              // image: res.data[0].image,
              author: 'server'
            })
          }
          else {
          // split overs here
            this.messages.push({
              text: msgtext,
              image: res.data[0].image,
              author: 'server'
            })

          }
          console.log('server says: ')
          console.log(res.data[0])
          this.$nextTick(() => {
            this.$refs.chatbox.scrollTop = this.$refs.chatbox.scrollHeight
            this.$refs.imgbox.scrollTop = this.$refs.imgbox.scrollHeight
          })
        })
      }
    },
    restart: function() {
      this.$axios.post('http://1.117.208.226:5005/webhooks/rest/webhook', {
          "message": '/restart',
          "sender": 'client'
      }, {timeout: 1000 * 60 * 4})
      .then(res => {
        this.messages = []
        this.$nextTick(() => {
          this.$refs.chatbox.scrollTop = this.$refs.chatbox.scrollHeight
          this.$refs.imgbox.scrollTop = this.$refs.imgbox.scrollHeight
          this.sender_id = uuidv4()
          console.log('update sender id: '+this.sender_id)
          function uuidv4() {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
              var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8)
              return v.toString(16)
            })
          }
        })
      })
    },
    upload(e) {
      let file = e.target.files[0]
      let param = new FormData() //创建form对象
      param.append('file',file) //通过append向form对象添加数据
      console.log(param.get('file')) //FormData私有类对象，访问不到，可以通过get判断值是否传进去
      this.$axios.post('http://1.117.208.226:8000/api/upload',param,{headers:{'Content-Type':'application/x-www-form-urlencoded' }}, {timeout: 1000 * 60 * 4} ) //请求头要为表单
      .then(response=>{
        console.log(response.data)
        let image_src = 'http://1.117.208.226:8000/static/images/' + response.data['filename']
        this.messages.push({
          image: image_src,
          author: 'client'
        })
        this.filename = response.data['filename']
        console.log('client says: ')
        console.log('upload_image: ' + this.filename)
        this.$nextTick(() => {
          this.$refs.chatbox.scrollTop = this.$refs.chatbox.scrollHeight
          this.$refs.imgbox.scrollTop = this.$refs.imgbox.scrollHeight
        })
        this.text = 'upload_image: ' + this.filename 
        this.$axios.post('http://1.117.208.226:5005/webhooks/rest/webhook', {
          "message": this.text,
          "sender": this.sender_id
        }, {timeout: 1000 * 60 * 4})
        .then(res => {
          this.messages.push({
            text: res.data[0].text,
            image: res.data[0].image,
            author: 'server'
          })
          console.log('server says: ')
          console.log(res.data[0])
          this.$nextTick(() => {
            this.$refs.chatbox.scrollTop = this.$refs.chatbox.scrollHeight
            this.$refs.imgbox.scrollTop = this.$refs.imgbox.scrollHeight
          })
        })
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    scroll(e) {
      this.$nextTick(() => {
        this.$refs.chatbox.scrollTop = this.$refs.chatbox.scrollHeight
        this.$refs.imgbox.scrollTop = this.$refs.imgbox.scrollHeight
        this.display = ''
      })
    },
    // background
    /* toggleTour(){
      this.$router.push({ path: '/tour', query: { q: 'email@kinski.com', t:'channel1' }});
    }, */
    showError(errId, errMsg) {
        alert('An error occured: ' + errId + ', ' + errMsg);
    },
    patchInitialized(patch) {
        // You can now access the patch object (patch), register variable watchers and so on
    },

    patchFinishedLoading(patch) {
      document.getElementById("container").classList.remove("loading");

      setTimeout(()=>{
        document.getElementById("loadingdisplay").remove();
      },500);
    },
    init(){
      new CABLES.Patch({
        patch: CABLES.exportedPatch,
        prefixAssetPath: '',
        glCanvasId: 'glcanvas',
        glCanvasResizeToWindow: true,
        onError: this.showError,
        onPatchLoaded: this.patchInitialized,
        onFinishedLoading: this.patchFinishedLoading,
      });
    },
  },
  created() {
      setTimeout(function () {
          L2Dwidget.init({
              model: {
                jsonPath: 'https://cdn.jsdelivr.net/gh/wangsrGit119/wangsr-image-bucket/L2Dwidget/live2d-widget-model-miku/assets/miku.model.json',
                scale: 1.5
              },
              dialog: {
                  // 开启对话框
                  enable: true,
                  script: {
                      // 当触摸到角色身体
                      'tap body': '哎呀！别碰我！',
                      // 当触摸到角色头部
                      'tap face': '人家是在认真写博客哦--前端妹子',
                  }
              },
              display: {
                position: 'left',
                width: 300,
                height: 600,
                hOffset: 30,
                vOffset: 100,
              },
          })
      },1000)
  }
}

// curl -XPOST -d '{"message":"hello","sender":"test"}' 'http://1.116.3.150:5005/webhooks/rest/webhook'
</script>

<style scoped>
.all {
  display: inline-flex;
  color: white;
}
.chat-box {
  display: flex;
  flex-direction: column;
  width: 40rem;
  height: 80vh;
  background: rgba(255,255,255,0.35);
  border-radius: 0.5rem;
  margin-left: 25%;
  margin-right: 3%;
  justify-content: space-between;
}
.chat-box-list {
  display: flex;
  flex-direction: column;
  list-style-type: none;
}
.chat-box-list-container{
  overflow-y: auto;
  scroll-behavior: smooth;
}
.chat-box-list {
  margin-top: 1rem;
  padding-left: 1rem;
  padding-right: 1rem;
  text-align: left;

}
.chat-box-list li {
  padding: 0.3rem;
  color: white;  
}
.chat-box-list div {
  display: flex;
  width: auto;
  height :auto;
  padding: 0.5rem;
  max-width: 80%;
  min-width: 0;
}
.chat-box-list .server div{
  float: left;
  background: #07f78c57;
  font-weight: 400;
  border-radius: 4px;
}
.chat-box-list .server img{
  float:left;
}
.chat-box-list .client div{
  float: right;
  flex-direction:row-reverse;
  background: rgba(0,0,0,0.5);
  border-radius: 4px;
}
.chat-box-list .client img{
  float:right;
}
.chat-inputs {
  display: flex;
  margin: 0 0 1rem 0;
  margin-top: 0;
  width: 85%;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.7);
  color: black;
}
.chat-inputs input {
  line-height: 2;
  width: 100%;
  border: 1px solid #999;
  border-left: none;
  border-bottom: none;
  border-right: none;
  border-top-left-radius: 20px;
  border-bottom-left-radius: 20px;
  padding-left: 1.5rem;
}
.chat-inputs input:focus {
  outline: none;
}
.restart {
  position: absolute;
  left: 20.7%;
  top: 22.35%;
  margin: 0;
}
.file {
  display: none;
}
.img-box {
  display: flex;
  flex-direction: column;
  width: 35rem;
  height: 80vh;
  border: 1px solid #39FF14;
  border-radius: 0.5rem;
  align-items: center;
}
.img-box-list-container{
  overflow-y: auto;
  scroll-behavior: smooth;
}
.img-box-list {
  list-style-type: none;
  padding: 0.5rem;
}
canvas {
  display: block;
  position: absolute;
  z-index: -1;
  left: 0;
  top: 0;
  padding: 0;
  margin: 0;
}
/* copied css */
.bn632-hover {
  width: 8rem;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  cursor: pointer;
  height: 2.5rem;
  text-align:center;
  border: none;
  background-size: 300% 100%;
  border-bottom-right-radius: 20px;
  border-top-right-radius: 20px;
  moz-transition: all .4s ease-in-out;
  -o-transition: all .4s ease-in-out;
  -webkit-transition: all .4s ease-in-out;
  transition: all .4s ease-in-out;
}

.bn632-hover:hover {
  background-position: 100% 0;
  moz-transition: all .4s ease-in-out;
  -o-transition: all .4s ease-in-out;
  -webkit-transition: all .4s ease-in-out;
  transition: all .4s ease-in-out;
}

.bn632-hover:focus {
  outline: none;
}

.bn632-hover.bn20 {
    background-image: linear-gradient(
      to right,
      #667eea,
      #764ba2,
      #6b8dd6,
      #8e37d7
    );
    box-shadow: 0 4px 15px 0 rgba(116, 79, 168, 0.75);
}
.bn6 {
  cursor: pointer;
  outline: none;
  border: none;
  background-color: #a164d6c9;
  padding: 0.6em 1.1em;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  font-weight: 300;
  color: #ffffff;
  background-size: 100% 100%;
  box-shadow: 3px 4px 12px 1px #ffffffa1;
}

.bn6:hover {
  background-image: linear-gradient(
    55deg,
    transparent 10%,
    #161616 10% 20%,
    transparent 20% 30%,
    #161616 30% 40%,
    transparent 40% 50%,
    #161616 50% 60%,
    transparent 60% 70%,
    #161616 70% 80%,
    transparent 80% 90%,
    #161616 90% 100%
  );
  animation: background 3s linear infinite;
}
.input {
  display: flex;
}
.upload_cover {
  position: relative;
  width: 2rem;
  height: 2rem;
  text-align: center;
  cursor: pointer;
  background: white;
  border: 1px solid #595656;
  border-radius: 100px;
  margin: 0.7em;
  margin-top: 0;
  top: 6%;
}
.upload_icon {
  font-size: 140%;
  position: absolute;
  left: 2%;
  width: 100%;
  top: 5%;
}
.display {
  color: white;
  position: absolute;
  width: 35rem;
  top: 40%;
  z-index: -1;
}
</style>

