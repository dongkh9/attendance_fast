<template>
<div v-if="showSoundModal" class="modal-overlay">
  <div class="modal-content">
      <p>🔔 출석 알림 소리를 재생하려면 버튼을 눌러주세요</p>
      <button @click="confirmSound">소리 허용</button>
  </div>
</div>
  <Navigation></Navigation>
<router-view></router-view>
</template>

<script setup>
import Navigation from "@/components/Navigation.vue"

import { onMounted, ref, onUnmounted, computed } from 'vue';
import { emitter } from '@/scripts/eventBus'
import AttendanceSound from "@/assets/sound/effect_attendance.mp3"

const evtSource = ref(null);
const showSoundModal = ref(sessionStorage.getItem('sound-confirmed') !== 'true')


const confirmSound = () => {
    playSound();
    showSoundModal.value = false;
    sessionStorage.setItem('sound-confirmed', 'true');
};

const playSound = () => {
    const audio = new Audio(AttendanceSound);
    audio.play();
};

const initSSE = () => {
    evtSource.value = new EventSource('http://localhost:8000/api/attendance/sse')
    evtSource.value.onmessage = (event) => {
    console.log('📡 출석 변경 감지됨:', event.data)
    if (event.data === 'AddAttendance') {
        playSound();
        emitter.emit('attendance-updated') 
    } else if (event.data === 'ping') {
        console.log('💓 서버 ping')
    }
    }
};

onMounted(async () => {
    initSSE();
});

onUnmounted(() => {
    evtSource.value?.close();
});
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0; left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0,0,0,0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}
.modal-content {
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    text-align: center;
}
.modal-content button {
    background-color: royalblue;
    color: white;
    padding: 10px 20px;
    border: none;
    font-weight: bold;
    border-radius: 6px;
    cursor: pointer;
}
</style>