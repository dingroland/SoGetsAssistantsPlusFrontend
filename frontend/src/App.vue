<template>
  <div id="app">
    <ChatApp />
  </div>
</template>

<script>
import ChatApp from "./components/ChatApp.vue";

export default {
  name: "App",
  components: { ChatApp },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  line-height: 1.5;
  background-color: #343541;
  color: #FFFFFF;
}

#app {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
}
</style>