<template>
  <v-container class="fill-height d-flex justify-left align-start flex-column">
    <v-overlay v-model="loading" absolute class="d-flex justify-center align-center" style="pointer-events: none;">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </v-overlay>
    <h1>タスク一覧</h1>
    <div v-for="item in todo" class="w-100">
      <v-card class="d-flex flex-row justify-space-between pa-3" flat>
        <div class="d-flex justify-center align-center">
          <v-checkbox :model-value="item.completed" @change="onChanged(item)">
            <template #details></template>
          </v-checkbox>
          <div>
            <v-card-title>
              {{ item.title }} <span style="font-size: 14px;">(期日: {{ item.deadline ?? "なし" }})</span>
            </v-card-title>
            <v-card-subtitle>
              {{ item.content }}
            </v-card-subtitle>
          </div>
        </div>
        <v-card-actions>
          <v-btn class="d-flex bg-error" v-bind="props" @click="remove(item.id)">
                <v-icon>
                  mdi-trash-can
                </v-icon>
              </v-btn>
          <v-dialog max-width="600px" v-model="editdialog">
            <template #activator="{ props }">
              <v-btn class="d-flex bg-primary" v-bind="props" @click="setEdit(item)">
                <v-icon>
                  mdi-pen
                </v-icon>
              </v-btn>
            </template>
            <v-card class="pa-10">
              <v-card-title>
                編集
              </v-card-title>
              <v-divider class="pb-10"/>
              <v-text-field label="タイトル" variant="underlined" v-model="editodo.title">
              </v-text-field>
              <v-text-field label="内容" variant="underlined" v-model="editodo.content">
              </v-text-field>
              <v-text-field label="期日" variant="underlined" v-model="editodo.deadline">
              </v-text-field>
              <v-card-actions>
                <v-btn class="bg-success" @click="update(item)">
                  <v-icon>
                    mdi-check
                  </v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-card-actions>
      </v-card>
    </div>
    <v-dialog max-width="600px" >
      <template #activator="{ props }">
        <div class="position-absolute" style="bottom: 50px; right: 50px;">
          <v-btn v-bind="props" class="pa-7 rounded-circle bg-success d-flex" icon="mdi-plus" size="30px" @click="setNew()" />
        </div>
      </template>
      <template #default="{ isActive }">
        <v-card class="pa-10">
          <v-card-title>
            新規作成
          </v-card-title>
          <v-divider class="pb-10"/>
          <v-text-field label="タイトル" variant="underlined" v-model="editodo.title">
          </v-text-field>
          <v-text-field label="内容" variant="underlined" v-model="editodo.content">
          </v-text-field>
          <v-text-field label="期日" variant="underlined" v-model="editodo.deadline">
          </v-text-field>
          <v-card-actions>
            <v-btn class="bg-success" @click="isActive.value = false; create()">
              <v-icon>
                mdi-check
              </v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </template>
    </v-dialog>
  </v-container>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';

const todo = ref((await axios.get("https://al1gt0bk9i.execute-api.ap-northeast-1.amazonaws.com/default/tasks")).data.items)
const loading = ref(false)
const editdialog = ref(false)
const editodo = ref({})

const setNew = () => {
  editodo.value = {
    title: "",
    content: "",
    deadline: ""
  }
}

const setEdit = (item) => {
  editdialog.value = true
  editodo.value = { ...item }
}

const create = async () => {
  loading.value = true
  editodo.value.id = (await axios.post("https://al1gt0bk9i.execute-api.ap-northeast-1.amazonaws.com/default/task", { ...editodo.value })).data.task_id
  todo.value.push({ ...editodo.value })
  editodo.value = {}
  loading.value = false
}

const update = async (item) => {
  loading.value = true
  await axios.put("https://al1gt0bk9i.execute-api.ap-northeast-1.amazonaws.com/default/task", item)
  todo.value[todo.value.findIndex(i => i.id == item.id)] = { ...editodo.value }
  loading.value = false
  editdialog.value = false
}


const remove = async (id) => {
  loading.value = true
  await axios.delete("https://al1gt0bk9i.execute-api.ap-northeast-1.amazonaws.com/default/task", {
    params: {
      id: id
    }
  })
  todo.value = todo.value.filter(t => t.id != id)
  loading.value = false
}

const onChanged = async (item) => {
  item.completed = !item.completed
  loading.value = true
  await axios.put("https://al1gt0bk9i.execute-api.ap-northeast-1.amazonaws.com/default/task", item)
  loading.value = false
}
</script>
