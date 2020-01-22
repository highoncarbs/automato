<template>
  <div>
    <div class="level">
      <div class="level-left">
        <p class="title">Scrapers</p>
      </div>
      <div class="level-right">
        <button class="button" @click="addModal = !addModal">
          <span class="icon icon-btn">
            <feather type="plus" size="1.3rem"></feather>
          </span>
          Add Scraper
        </button>
      </div>
    </div>
    <div class="level">
      <div class="level-left"></div>
      <div class="level-right"></div>
    </div>
    <br />
    <div class="box">
       <b-table
        :data="data"
      >
        <template slot-scope="props">
          <b-table-column field="id" label="ID" width="40">{{ props.row.id }}</b-table-column>

          <b-table-column field="city" label="City">{{ props.row.city[0].name }}</b-table-column>
          <b-table-column field="name" label="Tags">
            <span class="tag is-primary" style="margin-right:0.2rem" v-for="item in props.row.tag" :key="item.id">{{item.name }}</span> 
            </b-table-column>
          <b-table-column field="status" class="has-text-weight-bold" label="Status">{{ props.row.status | upper }}</b-table-column>
          <b-table-column field="Ttimestamp" label="Timestamp">{{ props.row.timestamp | date }}</b-table-column>

          <b-table-column field="action" label="Action">
            <div class="buttons">
              <button class="button is-small" @click="startItem(props.row.id)">
                <span class="icon">
                  <feather type="play" v-if="props.row.status == 'start'" size="1rem"></feather>
                  <feather type="refresh-cw" animation="spin" v-if="props.row.status == 'running'" size="1rem"></feather>
                  <feather type="repeat" v-if="props.row.status == 'done'" size="1rem"></feather>

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
    <NewScraper :view="addModal" v-on:closeModal="addModal = !addModal" />
  </div>
</template>

<script>
import NewScraper from "@/components/NewScraper";
export default {
  components: {
    NewScraper
  },
  computed: {},
  data() {
    return {
      addModal: false,
      data: []
    };
  },
  filters:{
    date: function(value){
      let d = new Date(value)
      return d.toDateString()
    },
    upper: function(value){
      return value.toUpperCase()
    }
  },
  mounted() {
    let self = this;
    this.$axios
      .get("/get/scraper")
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
  methods: {
    startItem(id){
      let self = this 
      this.$axios.get('/run/scraper/'+String(id))
        .then( function(response) {
          self.$buefy.snackbar.open({
          duration: 4000,
          message: "Unable to fetch data for City",
          type: "is-success",
          position: "is-top-right",
          actionText: "Close",
          queue: true,
          onAction: () => {
            self.isActive = false;
          }
        });
        })
    },
      deleteItem(id, index) {
      let self = this;
      this.$axios
        .$post("/delete/scraper/" + String(id))
        .then(function(response) {
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