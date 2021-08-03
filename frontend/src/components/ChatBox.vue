<template>
  <div>
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
            <img :id="idx" :src="message.image" v-show="!(message.image==null)" alt="image" style="width:65%"/>
          </li>
        </ul> 
      </div>
      <div class="chat-inputs">
        <input 
          type="text" 
          v-model="message" 
          @keyup.enter="sendMessage"
        />
        <button @click="sendMessage">Send</button>
      </div>
    </section>
    <button class="restart" v-on:click="restart">restart</button>
    <input class="file" name="file" type="file" accept="image/png,image/gif,image/jpeg" @change="upload"/>
    <!-- <input class="file" name="file" type="file" accept="image/png,image/gif,image/jpeg"/> -->
  </div>
</template>
  </div>
</template>

<script>
export default {
  name: 'ChatBox',
  data: () => ({
    message: '',
    text: '',
    messages: [],
    sender_id: '',
    filename: ''
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
        })
        this.$axios.post('http://1.117.208.226:5005/webhooks/rest/webhook', {
        // this.$axios.post('http://1.116.3.150:5005/webhooks/rest/webhook', {
        // this.$axios.post('http://localhost:5005/webhooks/rest/webhook', {
          "message": this.text,
          "sender": this.sender_id
        })
        .then(res => {
          this.messages.push({
            text: res.data[0].text,
            image: res.data[0].image,
            author: 'server'
          })
          console.log('server says: ')
          console.log(res.data[0]['text'])
          this.$nextTick(() => {
            this.$refs.chatbox.scrollTop = this.$refs.chatbox.scrollHeight
          })
        })
      }
    },
    restart: function() {
      this.$axios.post('http://1.117.208.226:5005/webhooks/rest/webhook', {
          "message": '/restart',
          "sender": 'client'
      })
      .then(res => {
        this.messages = []
        this.$nextTick(() => {
          this.$refs.chatbox.scrollTop = this.$refs.chatbox.scrollHeight
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
      this.$axios.post('http://1.117.208.226:8000/api/upload',param,{headers:{'Content-Type':'application/x-www-form-urlencoded' }}, ) //请求头要为表单
      .then(response=>{
        console.log(response.data)
        let image_src = 'http://1.117.208.226:8000/static/images/' + response.data['filename']
        this.messages.push({
          image: image_src,
          author: 'client'
        })
        this.filename = response.data['filename']
        console.log('client says: upload ')
        console.log(this.filename)
        this.$nextTick(() => {
          this.$refs.chatbox.scrollTop = this.$refs.chatbox.scrollHeight
        })
        this.text = 'upload_image: ' + this.filename 
        this.$axios.post('http://1.117.208.226:5005/webhooks/rest/webhook', {
          "message": this.text,
          "sender": this.sender_id
        })
        .then(res => {
          this.messages.push({
            text: res.data[0].text,
            image: res.data[0].image,
            author: 'server'
          })
          console.log('server says: ')
          console.log(res.data[0]['text'])
          this.$nextTick(() => {
            this.$refs.chatbox.scrollTop = this.$refs.chatbox.scrollHeight
          })
        })
      })
      .catch(function (error) {
        console.log(error)
      })
    },
  }
}

// curl -XPOST -d '{"message":"hello","sender":"test"}' 'http://1.116.3.150:5005/webhooks/rest/webhook'
</script>

<style scoped>
.chat-box,
.chat-box-list {
  display: flex;
  flex-direction: column;
  list-style-type: none;
}
.chat-box-list-container{
  overflow-y: auto;
  scroll-behavior: smooth;
}
.chat-box {
  width: 50%;
  height: 80vh;
  border: 1px solid #999;
  border-radius: 4px;
  margin-left: 10%;
  justify-content: space-between;
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
  background: green;
  border-radius: 4px;
}
.chat-box-list .server img{
  float:right;
}
.chat-box-list .client div{
  float: right;
  flex-direction:row-reverse;
  background: blue;
  border-radius: 4px;
}
.chat-box-list .client img{
  float:right;
}
.chat-inputs {
  display: flex;
}
.chat-inputs input {
  line-height: 3;
  width: 100%;
  border: 1px solid #999;
  border-left: none;
  border-bottom: none;
  border-right: none;
  border-bottom-left-radius: 4px;
  padding-left: 1.5rem;
}
.chat-inputs button {
  width: 8rem;
  color: white;
  background: rgb(45, 110, 167);
  border-bottom-right-radius: 4px;
}
.restart {
  position: absolute;
  left: 10%;
}
.file {
  position: absolute;
  left: 20%;
}
</style>

