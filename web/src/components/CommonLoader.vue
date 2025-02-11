<template>
  <v-progress-circular
    color="teal"
    indeterminate
    :size="70"
    :width="7"
    class="common-loader"
  />
</template>

<style lang="scss">
.common-loader {
  display: flex;
  margin: 50% auto 0;
}
</style>