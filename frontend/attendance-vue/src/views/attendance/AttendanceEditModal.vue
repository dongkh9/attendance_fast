<template>
    <div class="modal-backdrop">
      <div class="modal">
        <h2>{{ mode === 'edit' ? '출석 수정' : '출석 추가' }}</h2>

        <form @submit.prevent="submit">
          <div v-if="mode === 'create'">
            <label>교육생 검색
              <input
                type="text"
                v-model="studentSearch"
                placeholder="이름 입력..."
              />
            </label>

            <label>교육생 선택
              <select v-model="localData.student_id" required>
                <option value="">선택하세요</option>
                <option v-for="student in filteredStudents" :key="student.id" :value="student.id">
                  {{ student.name }}
                </option>
              </select>
            </label>
          </div>

          <label>입실시간
            <input
              type="text"
              v-model="checkIn"
              placeholder="HH:MM"
              required
            />
          </label>
          <label>퇴실시간
            <input
              type="text"
              v-model="checkOut"
              placeholder="HH:MM"
            />
          </label>
          <div class="modal-actions">
            <button type="submit">저장</button>
            <button type="button" @click="emit('close')">닫기</button>
          </div>
        </form>
      </div>
    </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import axios from 'axios';

const props = defineProps({
  mode: String,
  attendanceData: Object
});
const emit = defineEmits(['close', 'saved']);

const localData = ref({
  check_in: '',
  check_out: '',
  status: '출석'
});

const studentSearch = ref('');
const allStudents = ref([]); // 부모에서 props로 전달해도 되고, fetch해도 됨

// 교육생 리스트 필터링
const filteredStudents = computed(() => {
  return allStudents.value.filter(student =>
    student.name.includes(studentSearch.value.trim())
  );
});

const checkIn = computed({
  get: () => localData.value.check_in,
  set: (val) => {
    localData.value.check_in = val.slice(0, 5);
  }
});

const checkOut = computed({
  get: () => localData.value.check_out,
  set: (val) => {
    localData.value.check_out = val.slice(0, 5);
  }
});

watch(
  () => props.attendanceData,
  (val) => {
    if (val) {
      localData.value = {
        attendance_id: val.id,
        course_id: val.course_id,
        student_id: val.student_id,
        date: val.date,
        check_in: val.check_in?.slice(0, 5) || '',
        check_out: val.check_out?.slice(0, 5) || '',
        status: val.status || '출석'
      };
    } else {
      localData.value = {
        id: null,
        check_in: '',
        check_out: '',
        status: '출석'
      };
    }
  },
  { immediate: true }
);

watch(
  () => localData.value.student_id,
  (id) => {
    const selected = allStudents.value.find(s => s.id === id);
    if (selected) {
      studentSearch.value = selected.name;
      localData.value.course_id = selected.course_id; // ✅ 여기 추가

    }
  }
);


const timeRegex = /^([01]\d|2[0-3]):[0-5]\d$/;

const submit = () => {
  if (!timeRegex.test(localData.value.check_in)) {
    alert("입실시간은 HH:MM 형식으로 입력해주세요.");
    return;
  }
  if (localData.value.check_out && !timeRegex.test(localData.value.check_out)) {
    alert("퇴실시간은 HH:MM 형식으로 입력해주세요.");
    return;
  }

  if (localData.value.check_in && !localData.value.check_out) {
    localData.value.status = '입실';
  } else if (localData.value.check_in && localData.value.check_out) {
    localData.value.status = '퇴실';
  }

  if (props.mode === 'edit') {
    emit('saved', localData.value);
  } else if (props.mode === 'create') {
    emit('created', localData.value);
  }

  emit('close');
};


onMounted( async ()=>{
    const response = await axios.get("/student/")
    allStudents.value = response.data;
    console.log(allStudents);
})
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0; left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}
.modal {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  min-width: 300px;
  box-shadow: 0 0 10px rgba(0,0,0,0.2);
}
label {
  display: block;
  margin: 1rem 0;
  font-size: 0.9rem;
}
input, select {
  width: 100%;
  padding: 6px;
  margin-top: 4px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 1rem;
}
button {
  padding: 6px 12px;
  border: none;
  background-color: royalblue;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}
button[type="button"] {
  background-color: #ccc;
  color: black;
}
</style>
