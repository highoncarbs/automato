<template>
  <div>
    <div class="level">
      <div class="level-left">
        <p class="title">Groups</p>
      </div>
      <div class="level-right">
        <button class="button" @click="addModal = !addModal">
          <span class="icon icon-btn">
            <feather type="plus" size="1.3rem"></feather>
          </span>
          New Group
        </button>
        <button class="button level-item" @click="getData">
          <span class="icon icon-btn">
            <feather type="refresh-cw" size="1.3rem"></feather>
          </span>
          Refresh
        </button>
      </div>
    </div>
    <div class="level">
      <div class="level-left"></div>
      <div class="level-right"></div>
    </div>
    <br />
    <div class="box">
      <b-table :data="data">
        <template slot-scope="props">
          <b-table-column field="name" label="Name">{{ props.row.name }}</b-table-column>
          <b-table-column field="contacts" label="Total">
            <span
              class="tag has-text-weight-bold"
              v-if="props.row.total.contact != 0"
            >{{ props.row.total.contact }}</span>
            <span
              class="tag has-text-weight-bold"
              v-if="props.row.total.tag != 0"
            >{{ props.row.total.tag }}</span>
            <span
              class="tag has-text-weight-bold"
              v-if="props.row.total.tag == 0 && props.row.total.contact == 0"
            >0</span>
          </b-table-column>
          <b-table-column field="city" label="City">
            <span
              class="tag is-primary"
              style="margin-right:0.2rem"
              v-for="item in props.row.city"
              :key="item.id"
            >{{item.name }}</span>
          </b-table-column>
          <b-table-column field="tag" label="Tag">
            <span
              class="tag is-primary"
              style="margin-right:0.2rem"
              v-for="item in props.row.tag"
              :key="item.id"
            >{{item.name }}</span>
          </b-table-column>
          <b-table-column field="action" label="Action">
            <div class="buttons">
              <button class="button is-small" @click="pauseItem(props.row.id)">
                <span class="icon">
                  <feather type="eye" size="1rem"></feather>
                </span>
              </button>
              <button class="button is-small" @click="startItem(props.row.id)">
                <span class="icon">
                  <feather type="edit" size="1rem"></feather>
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
    <NewGroup :view="addModal" v-on:closeModal="addModal = !addModal" />
  </div>
</template>

<script>
import NewGroup from "@/components/NewGroup";
export default {
  components: {
    NewGroup
  },
  computed: {},
  data() {
    return {
      addModal: false,
      data: []
    };
  },
  filters: {
    date: function(value) {
      let d = new Date(value);
      return d.toDateString();
    },
    upper: function(value) {
      return value.toUpperCase();
    }
  },
  mounted() {
    this.getData();
  },
  methods: {
    getData() {
      let self = this;
      this.$axios
        .get("/get/club")
        .then(function(response) {
          console.log(response.data);
          self.data = response.data;
        })
        .catch(function(error) {
          console.log(error);
          self.$buefy.snackbar.open({
            duration: 4000,
            message: "Unable to fetch data for City",
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
      this.$axios.$post("/delete/club/" + String(id)).then(function(response) {
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
    }
  }
};
</script>