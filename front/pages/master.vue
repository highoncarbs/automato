<template>
  <div>
    <div class="level">
      <div class="level-left">
        <p class="title">Master</p>
      </div>
    </div>
    <br />
    <div class="tabs is-toggle is-fullwidth">
      <ul>
        <li :class=" {'is-active' : active == 'city'} " @click="active = 'city' ">
          <NuxtLink to="/master/city" >City</NuxtLink>
        </li>
        <li  :class=" {'is-active' : active == 'tag'} "  @click="active = 'tag' ">
          <NuxtLink to="/master/tag">Tags</NuxtLink>
        </li>
      </ul>
    </div>
    <br />
    <NuxtChild :key="$route.params" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      active : "city"
    };
  }
};
</script>

<style  scoped>
  .is-active > a{
    background-color: black !important;
    border-color: black !important;
  }
</style>