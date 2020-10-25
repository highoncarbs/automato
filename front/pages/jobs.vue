<template>
  <div>
    <div class="level">
      <div class="level-left">
        <p class="title">Jobs</p>
      </div>
      <div class="level-right">
        <button class="button level-item" @click="addModal = !addModal">
          <span class="icon icon-btn">
            <feather type="plus" size="1.3rem"></feather>
          </span>
          Add Job
        </button>
        <button class="button level-item" @click="getData">
          <span class="icon icon-btn">
            <feather type="refresh-cw" size="1.3rem"></feather>
          </span>
          Refresh
        </button>
      </div>
    </div>
   <div class="notification is-warning is-small is-narrow has-text-weight-medium">
     <span class="icon icon-btn">
       <feather type="info" size="1.3rem" />
     </span>
     We advise you to run a Whatsapp job only once per device a day ( Limited to 100 Messages/day )
   </div>
    
    <div class="box">
      <b-table :data="data">
        <template slot-scope="props">
          <b-table-column field="id" label="ID" width="40">{{ props.row.id }}</b-table-column>

          <b-table-column field="city" label="Template">{{ props.row.template[0].name }}</b-table-column>
          <b-table-column field="group" label="Groups">
            <span
              class="tag is-primary"
              style="margin-right:0.2rem"
              v-for="item in props.row.club"
              :key="item.id"
            >{{item.name }}</span>
          </b-table-column>
          <b-table-column
            field="status"
            class="has-text-weight-bold"
            label="Status"
          >{{ props.row.status | upper }}</b-table-column>
          <b-table-column field="type" label="Type">
            <span
              class="tag is-info has-text-weight-bold"
              style="margin-right:0.2rem"
            >{{ getType(props.row.meta) | upper }}</span>
          </b-table-column>

          <b-table-column field="Ttimestamp" label="Timestamp">{{ props.row.timestamp | date }}</b-table-column>
          <b-table-column field="Last Run" label="Last Run">{{ getLast(props.row.meta)}}</b-table-column>

          <b-table-column field="action" label="Action">
            <div class="buttons">
              <button class="button is-small" v-if="getType(props.row.meta) ==='whatsapp' " @click="startItem(props.row.id)">
                <span class="icon">
                  <feather type="play" v-if="props.row.status == 'start'" size="1rem"></feather>
                  <feather type="repeat" v-if="props.row.status == 'done'" size="1rem"></feather>
                  <feather
                    type="refresh-cw"
                    animation="spin"
                    v-if="props.row.status == 'running'"
                    size="1rem"
                  ></feather>
                </span>
              </button>
              <button class="button is-small" v-if="getType(props.row.meta) ==='sms' " @click="startSmsItem(props.row.id)">
                <span class="icon">
                  <feather type="play" v-if="props.row.status == 'start'" size="1rem"></feather>
                  <feather type="repeat" v-if="props.row.status == 'done'" size="1rem"></feather>
                  <feather
                    type="refresh-cw"
                    animation="spin"
                    v-if="props.row.status == 'running'"
                    size="1rem"
                  ></feather>
                </span>
              </button>
              <button class="button is-small" @click="pauseItem(props.row.id)">
                <span class="icon">
                  <feather type="pause" size="1rem"></feather>
                </span>
              </button>
              <button
                class="button is-danger is-small"
                @click="deleteItem(props.row.id , props.index)"
              >
                <span class="icon">
                  <feather type="x" size="1rem"></feather>
                </span>
              </button>
            </div>
          </b-table-column>
        </template>
      </b-table>
    </div>
    <NewJob :view="addModal" v-on:closeModal="addModal = !addModal" />

    <!-- Job Run Modal -->
    <div class="modal" :class="{ 'is-active' : runModal }">
      <div class="modal-background" @click="runModal = !runModal"></div>
      <div class="modal-content">
        <div class="box has-text-centered" style="margin-bottom : 0px;">
          <p class="title has-text-weight-bold">Ready . Set . Go!</p>
          <br />
          <br />
          <p class="is-size-5 has-text-weight-semibold">
            Keep your smartphone ready for a Whatsapp Web Scan. Follow
            the steps below :
          </p>
          <br />
          <div class="notification is-light has-text-centered">
            Select timer according to your network and device. Fast Networks and newer devices require less time.
            <br />
            <br />
            <b-field position="is-centered">
              <b-radio-button v-model="timer" native-value="20" type="is-black">
                <span>20</span>
              </b-radio-button>

              <b-radio-button v-model="timer" native-value="25" type="is-black">
                <span>25</span>
              </b-radio-button>
              <b-radio-button v-model="timer" native-value="30" type="is-black">
                <span>30</span>
              </b-radio-button>
              <b-radio-button v-model="timer" native-value="35" type="is-black">
                <span>35</span>
              </b-radio-button>
            </b-field>
          </div>

          <div class="content has-text-left">
            <ul class>
              <li>Open Whatsapp on your Phone</li>
              <li>
                Tap
                <span class="has-text-weight-bold">menu</span> or
                <span class="has-text-weight-bold">settings</span> and select
                <span class="has-text-weight-bold">
                  Whatsapp
                  Web
                </span>
              </li>
              <li>Point your phone to the whatsapp webpage that'll open soon.</li>
              <li>That's it !</li>
            </ul>
          </div>
          <a class="button is-black" @click="runItem">
            <span class="icon icon-btn">
              <feather type="play-circle" size="1.3rem" />
            </span>Start
          </a>
        </div>
      </div>
      <div class="modal-close" @click="runModal = !runModal"></div>
    </div>
  </div>
</template>
<script>
import NewJob from "@/components/NewJob";
export default {
  components: {
    NewJob
  },
  data() {
    return {
      timer: "25",
      addModal: false,
      runModal: false,
      data: [],
      current_id: ""
    };
  },
  mounted() {
    this.getData();
  },
  methods: {
    getData() {
      let self = this;
      this.$axios
        .get("/get/job")
        .then(function(response) {
          console.log("Here job" + response.data);
          self.data = response.data;
        })
        .catch(function(error) {
          console.log(error);
          self.$buefy.snackbar.open({
            duration: 4000,
            message: "Unable to load Jobs",
            type: "is-light",
            position: "is-top-right",
            actionText: "Close",
            queue: true,
            onAction: () => {
              self.isActive = false;
            }
          });
        });
    },
    getType(val) {
      let data = JSON.parse(val);
      if (data.hasOwnProperty("type")) {
        return data["type"];
      } else {
        return "whatsapp";
      }
    },
    getLast(val) {
      let data = JSON.parse(val);
      if (data.hasOwnProperty("last")) {
        return data["last"];
      } else {
        return 0;
      }
    },
    startItem(id) {
      this.runModal = !this.runModal;
      this.current_id = parseInt(id);
    },
    startSmsItem(id){
      let self = this;
      let form = { curr_id: id };

      this.$axios
        .post("/run/job/sms" , form)
        .then(function(response) {
          if (response.data.success) {
            console.log(response);
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
        })
        .catch(function(error) {
          console.log(error);
          self.$buefy.snackbar.open({
            duration: 4000,
            message: response.data.message ,
            type: "is-light",
            position: "is-top-right",
            actionText: "Close",
            queue: true,
            onAction: () => {
              self.isActive = false;
            }
          });
        });
    },
    deleteItem(id, index) {
      let self = this;
      this.$axios.$post("/delete/job/" + String(id)).then(function(response) {
        if (response.success) {
          self.data.splice(index, 1);
          self.$buefy.snackbar.open({
            duration: 4000,
            message: response.success,
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
            message: response.message,
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
    runItem() {
      let self = this;
      let form = { curr_id: this.current_id, timer: this.timer };
      this.$axios
        .post("/run/job", form)
        .then(function(response) {
          if (response.success) {
            console.log(response);
            self.runModal = false;
            self.$buefy.snackbar.open({
              duration: 4000,
              message: response.success,
              type: "is-light",
              position: "is-top-right",
              actionText: "Close",
              queue: true,
              onAction: () => {
                self.isActive = false;
              }
            });
          }
        })
        .catch(function(error) {
          console.log(error);
          self.$buefy.snackbar.open({
            duration: 4000,
            message: "Unable to load Jobs",
            type: "is-light",
            position: "is-top-right",
            actionText: "Close",
            queue: true,
            onAction: () => {
              self.isActive = false;
            }
          });
        });
    }
  },
  filters: {
    date: function(value) {
      let d = new Date(value);
      return d.toDateString();
    },
    upper: function(value) {
      return value.toUpperCase();
    }
  }
};
</script>