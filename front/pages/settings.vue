<template>
  <div>
    <div class="level">
      <div class="level-left">
        <p class="title">Settings</p>
      </div>
    </div>

    <br />
    <div class="box">
      <div class="field">
        <label class="label">
          <p class="is-size-4">Selenium Webdriver</p>
          <p class="is-size-6 has-text-grey has-text-weight-semibold">
            Copy the path to your Selenium Webdriver ( Chrome )
            <span
              class="tag is-warning"
            >Firefox/Gecko not supported yet</span>
          </p>
        </label>
        <div class="control">
          <input type="text" placeholder="Webdriver path" class="input" />
        </div>
      </div>

      <hr />
      <div class="notification is-danger-light">
        <div class="field">
          <label class="label">
            <p class="is-size-4">Delete Saved Whatsapp Session</p>
            <p
              class="is-size-6 has-text-grey has-text-weight-semibold"
            >Deletes your whatsapp login information. Delete if you want to use another phone.</p>
          </label>
          <div class="control">
            <button class="button is-danger" @click="clearUserInfoWhatsapp">
              <span class="icon icon-btn">
                <feather type="trash" size="1.3rem " />
              </span>
              Delete Whatsapp Login
            </button>
          </div>
        </div>
        <br />
        <div class="field">
          <label class="label">
            <p class="is-size-4">Delete Saved Google Messages/SMS Session</p>
            <p
              class="is-size-6 has-text-grey has-text-weight-semibold"
            >Deletes your Google Messages login information. Delete if you want to use another phone.</p>
          </label>
          <div class="control">
            <button class="button is-danger" @click="clearUserInfoSms">
              <span class="icon icon-btn">
                <feather type="trash" size="1.3rem " />
              </span>
              Delete Messages Login
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {
    clearUserInfoWhatsapp() {
      let self = this;
      this.$axios.post("/settings/clearlogins/whatsapp").then(function(response) {
        console.log(response);
        if (response.data.success) {
          self.$buefy.snackbar.open({
            duration: 4000,
            message: response.data.success,
            type: "is-light",
            position: "is-top-right",
            actionText: "Close",
            queue: true,
            onAction: () => {
              self.isActive = false;
            }
          });
        } else {
          self.$buefy.snackbar.open({
            duration: 4000,
            message: response.data.success,
            type: "is-light",
            position: "is-top-right",
            actionText: "Close",
            queue: true,
            onAction: () => {
              self.isActive = false;
            }
          });
        }
      });
    },
    clearUserInfoSms() {
      let self = this;
      this.$axios.post("/settings/clearlogins/sms").then(function(response) {
        console.log(response);
        if (response.data.success) {
          self.$buefy.snackbar.open({
            duration: 4000,
            message: response.data.success,
            type: "is-light",
            position: "is-top-right",
            actionText: "Close",
            queue: true,
            onAction: () => {
              self.isActive = false;
            }
          });
        } else {
          self.$buefy.snackbar.open({
            duration: 4000,
            message: response.data.success,
            type: "is-light",
            position: "is-top-right",
            actionText: "Close",
            queue: true,
            onAction: () => {
              self.isActive = false;
            }
          });
        }
      });
    }
  }
};
</script>