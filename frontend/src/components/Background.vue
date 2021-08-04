<template>
  <div id="app">
    <div id="loadingdisplay">Loading...</div>
    <div id="container" class="loading">
      <canvas id="glcanvas" width="100vw" height="100vh"></canvas>
    </div>
    <router-view></router-view>
  </div>
</template>
<script>
export default {
  name: 'App',
  components: {
  },
  props:['q'],
  watch:{
    $route(to, from)  {
    }
  },
  methods:{
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
  updated(){
  },
  created() {
  },
  mounted() {
    let script = document.createElement('script')
    script .setAttribute('src', '@/assets/patch.js')
    this.$el.appendChild(script);
    document.addEventListener('CABLES.jsLoaded',  event => {
      console.log('cables loaded')
      setTimeout(() =>{ this.init() },1500);
    })
  },
}
</script>

<style>
body{
  margin:0px;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  width: 100%;
  height: 100%;
  padding: 0px;
  margin: 0px;
}

 *
    {
        user-select: none;
    }
    body {
        margin: 0;
        background-color: #fff;
        color: #444;
        font-family: Helvetica, Arial, sans-serif;
        overflow: hidden;
    }
     canvas {
      display: block;
      position: absolute;
    }
    footer {
        position: absolute;
        bottom: 0;
        left: 0;
        box-sizing: border-box;
        width: 100vw;
        padding: 20px;
        text-align: right;
        font-size: 18px;
        color: #24baa7;
    }

    footer a,
    footer a:hover,
    footer a:active {
        color: #24baa7;
    }

    .loading div
    {
        display:none !important;
    }

    #loadingdisplay
    {
        position:absolute;
        top:50%;
        text-align: center;
        width:100%;
    }
    .call-icon-button{
        cursor: pointer;
        position: absolute;
        z-index: 995!important;
        border-radius: 100%;
        background-color: #fff;
        width: 50px;
        height: 50px;
        bottom: 20px;
        right: 90px;
        text-align: center;
    }

</style>