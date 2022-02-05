<template>
  <div id="app">
    <credit-form></credit-form>
  </div>
</template>

<script>
  import CreditForm from "@/components/CreditForm";

export default {

  name: 'App',
  components: {
    CreditForm
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
