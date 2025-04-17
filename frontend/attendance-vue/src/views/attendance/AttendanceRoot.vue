<template>

<AttendanceEditModal
    v-if="showModal"
    :mode="modalMode"
    :attendanceData="selectedAttendance"
    @close="showModal = false"
    @saved="submitEdit"
    @created="submitPost"
/>

    <div class="course-container">
        <div class="course-info" v-for="course in todayCourseList" :key="course.id">
            <span class="course-name">{{ course.name }}</span>
            <span class="course-counts">
                <span>총원 {{ course.student_count }}</span>
                <span>입실 {{ attendanceStats[course.id]?.checkIn || 0 }}</span>
                <span>퇴실 {{ attendanceStats[course.id]?.checkOut || 0 }}</span>
            </span>
        </div>
    </div>

    <div class="board-controls">
        <label>
            과정 필터:
            <select v-model="filters.course">
                <option value="">전체</option>
                <option v-for="course in todayCourseList" :key="course.id" :value="course.name">{{ course.name }}</option>
            </select>
        </label>
        <label>
            출석구분:
            <select v-model="filters.status">
                <option value="">전체</option>
                <option value="출석">출석</option>
                <option value="입실">입실</option>
                <option value="지각">지각</option>
                <option value="퇴실">퇴실</option>
            </select>
        </label>
    </div>

    <div class="board-container">
        <div class="board-table-header board-tr">
            <div class="th" @click="toggleSort('student_name')"
            :class="{sorted: sortState.key === 'student_name' && sortState.direction !== 0,
            descending: sortState.key === 'student_name' && sortState.direction === -1}">
            이름</div>
            <div class="th" @click="toggleSort('course_name')"
            :class="{sorted: sortState.key === 'course_name' && sortState.direction !== 0,
            descending: sortState.key === 'course_name' && sortState.direction === -1}">
            과정</div>
            <div class="th" @click="toggleSort('phone')">
            전화번호</div>
            <div class="th" @click="toggleSort('check_in')"
            :class="{sorted: sortState.key === 'check_in' && sortState.direction !== 0,
            descending: sortState.key === 'check_in' && sortState.direction === -1}">
            입실시간</div>
            <div class="th" @click="toggleSort('check_out')"
            :class="{sorted: sortState.key === 'check_out' && sortState.direction !== 0,
            descending: sortState.key === 'check_out' && sortState.direction === -1}">
            퇴실시간</div>
            <div class="th">참여시간</div>
            <div class="th" @click="toggleSort('status')"
            :class="{sorted: sortState.key === 'status' && sortState.direction !== 0,
            descending: sortState.key === 'status' && sortState.direction === -1}">
            출석구분</div>
            <div class="th"></div>
            <div class="th">
              <span>
                <button class="add-button" @click="openModal('create')">
                  <i class="fas fa-plus"></i>
                </button>
              </span>
            </div>
        </div>
        <div class="board-body">
            <div class="board-tr" v-for="attendance in filteredAndSortedAttendance" :key="attendance.id">
                <div class="td">{{ attendance.student_name }}</div>
                <div class="td">{{ attendance.course_name }}</div>
                <div class="td">{{ attendance.phone }}</div>
                <div class="td">{{ attendance.check_in }}</div>
                <div class="td">{{ attendance.check_out }}</div>
                <div class="td">{{ getDuration(attendance.check_in, attendance.check_out) }}</div>
                <div class="td">{{ attendance.status }}</div>
                <div class="td">
                    <button class="edit-button" @click="openModal('edit',attendance)">
                        <i class="fas fa-edit"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref, onUnmounted, computed } from 'vue';
import axios from 'axios';
import { emitter } from '@/scripts/eventBus';
import AttendanceEditModal from './AttendanceEditModal.vue';

const todayAttendanceList = ref([]);
const todayCourseList = ref([]);
const showModal = ref(false);
const modalMode = ref('create');
const selectedAttendance = ref(null);

const openModal = (mode, data=null) => {
    modalMode.value = mode;
    selectedAttendance.value = data;
    showModal.value = true;
};

const filters = ref({ course: '', status: '' });
const sortState = ref({ key: '', direction: 1 });

const attendanceStats = computed(() => {
    const map = {};
    for (const attendance of todayAttendanceList.value) {
        const cid = attendance.course_id;
        const status = attendance.status;
        if (!map[cid]) map[cid] = { checkIn: 0, checkOut: 0 };
        if (["입실", "출석", "지각"].includes(status)) map[cid].checkIn++;
        else if (status === "퇴실") map[cid].checkOut++;
    }
    return map;
});

const getDuration = (checkIn, checkOut) => {
    if (!checkIn || !checkOut) return '-';
    const inTime = new Date(`1970-01-01T${checkIn}`);
    const outTime = new Date(`1970-01-01T${checkOut}`);
    const diffMs = outTime - inTime;
    if (diffMs < 0) return '-';
    const h = Math.floor(diffMs / 1000 / 60 / 60).toString().padStart(2, '0');
    const m = Math.floor((diffMs / 1000 / 60) % 60).toString().padStart(2, '0');
    return `${h}:${m}`;
};

const toggleSort = (key) => {
  if (sortState.value.key === key) {
    // 1 → -1 → 0 (정렬 해제)
    if (sortState.value.direction === 1) {
      sortState.value.direction = -1;
    } else if (sortState.value.direction === -1) {
      sortState.value.key = '';
      sortState.value.direction = 0;
    }
  } else {
    sortState.value.key = key;
    sortState.value.direction = 1;
  }
};

const filteredAndSortedAttendance = computed(() => {
    let result = [...todayAttendanceList.value];

    if (filters.value.course) {
        result = result.filter(item => item.course_name === filters.value.course);
    }
    if (filters.value.status) {
        result = result.filter(item => item.status === filters.value.status);
    }

    if (sortState.value.key && sortState.value.direction !== 0) {
  result.sort((a, b) => {
    const dir = sortState.value.direction;
    if (a[sortState.value.key] < b[sortState.value.key]) return -1 * dir;
    if (a[sortState.value.key] > b[sortState.value.key]) return 1 * dir;
    return 0;
  });
}


    return result;
});

const fetchAttendnace = async () => {
    const response = await axios.get("attendance/list/today");
    todayAttendanceList.value = response.data;
};

const fetchCourse = async () => {
    const response = await axios.get("course/list");
    const allCourses = response.data;
    const today = new Date().getDay();
    const dayMap = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
    const todayCode = dayMap[today];
    todayCourseList.value = allCourses.filter(course => {
        const weekDays = typeof course.week_days === "string" ? course.week_days.split(",") : course.week_days;
        return weekDays.includes(todayCode);
    });
};

const submitEdit = async (data) => {
  const payload = {
    course_id: data.course_id,
    student_id: data.student_id,
    date: data.date,
    check_in: data.check_in + ":00",
    status: data.status
  };

  if (data.check_out) {
    payload.check_out = data.check_out + ":00";
  }

  await axios.put(`attendance/${data.attendance_id}`, payload);
  await fetchAttendnace();

};

const submitPost = async (data) => {
  const today = new Date();
  const year = today.getFullYear().toString().slice(-2);
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const day = String(today.getDate()).padStart(2, '0');
  const formattedDate = `${year}-${month}-${day}`;

const payload = {
  course_id: data.course_id,
  student_id: data.student_id,
  date: formattedDate,
  check_in: data.check_in + ":00",
  status: data.status
};


  if (data.check_out) {
    payload.check_out = data.check_out + ":00";
  }
  console.log(data);
  await axios.post(`attendance`, payload);
  await fetchAttendnace();

};


onMounted(async () => {
    await fetchCourse();
    await fetchAttendnace();
    emitter.on('attendance-updated', fetchAttendnace);
});

onUnmounted(() => {
    emitter.off('attendance-updated', fetchAttendnace);
});
</script>

<style scoped>
.course-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  gap: 0.7vh 1vw;
  margin: 0.5vh 5vw;
  width: 90%;
  padding: 1vh 1vw;
  background-color: rgba(65, 105, 225, 0.07);
  border-radius: 8px;
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.08);
  font-size: 0.9rem;
  height: auto;
}

.course-info {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5vw;
  min-width: 220px;
  max-width: 300px;
  padding: 0.6vh 1vw;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 6px;
  background-color: white;
  box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease;
}

.course-name {
  font-weight: bold;
  color: #2c3e50;
}

.course-counts {
  display: flex;
  gap: 0.5vw;
  color: #444;
  font-weight: 500;
  flex-wrap: wrap;
}

.board-controls {
  display: flex;
  gap: 1rem;
  margin: 10px 5vw;
  font-size: 0.9rem;
}

label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

select {
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.board-container {
  height: 65vh;
  overflow-y: auto;
  width: 100%;
  max-width: 90%;
  margin-left: 5vw;
  margin-right: 5vw;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.board-table-header {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr 1fr 0.3fr 0.3fr;
    position: sticky;   
  top: 0;
  background-color: royalblue;
  z-index: 10;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
  cursor: pointer;
}

.board-body {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  width: 100%;
}

.board-tr {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr 1fr 0.3fr 0.3fr;
  width: 100%;
}

.th, .td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.board-tr:nth-child(even) {
  background-color: #f9f9f9;
}

.th.sorted {
  background-color: #f1f1f1;
  font-weight: bold;
  color: #2c3e50;
}

.th.sorted::after {
  content: " ▲";
  font-size: 0.8em;
  color: #007bff;
}

.th.sorted.descending::after {
  content: " ▼";
}

.edit-button{
    border: none;
    cursor: pointer;
}

.edit-button:hover{
    background-color: royalblue;
}

.add-button {
  border: none;
  background-color: rgb(255, 128, 130);
  color: white;
  padding: 6px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.add-button:hover {
  background-color: #fb0505;
}


</style>