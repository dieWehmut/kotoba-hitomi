<!-- filepath: vue-chat/src/components/chat/chatScreen/BaseChat.vue -->
<template>
  <section :id="chatId" class="screen">
    <GuideModal v-if="showGuide" :mode="mode" @close="showGuide = false" />
    <!-- 文件预览模态框 -->
    <div v-if="showFileModal" class="file-modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <h3>{{ modalTitle }}</h3>
        <img v-if="isImage" :src="modalContent" class="file-preview-image" />
        <textarea
          v-else
          v-model="editableContent"
          class="file-content-editor"
          :placeholder="isImage ? '图片不可编辑' : '在此编辑文件内容'"
        ></textarea>
        <button v-if="!isImage" class="anime-btn save-btn" @click="saveChanges">
          保存
        </button>
      </div>
    </div>
    <div class="lefttop-container">
      <div class="lefttop-first-container">
        <button class="anime-btn back-btn" @click="$emit('back')">
          <i class="fas fa-arrow-left"></i>
        </button>
      </div>
      <div class="lefttop-second-container">
        <button
          v-show="sessionCollapsed"
          class="expand-btn"
          @click="sessionCollapsed = !sessionCollapsed"
        >
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>

      <transition name="slide">
        <div v-show="!sessionCollapsed" class="session-sidebar">
          <div class="sessions-header">
            <h3>{{ $t("baseChat.history") }}</h3>
            <button class="anime-btn" @click="createNewChat">
              <i class="fas fa-plus"></i>
            </button>
            <!-- 合并后的背景设置按钮 -->
            <button
              class="anime-btn"
              @click.stop="showBgOptions = !showBgOptions"
            >
              <i class="fas fa-palette"></i>
            </button>

            <!-- 背景选项弹出层 -->
            <transition name="fade">
              <div v-if="showBgOptions" class="bg-options-menu">
                <div class="bg-option" @click="toggleBackground">
                  <i class="fas fa-image"></i> {{ $t("baseChat.customBg") }}
                  <input
                    type="file"
                    ref="bgInput"
                    accept="image/*"
                    @change="setBackgroundFromInput"
                    style="display: none"
                  />
                </div>
                <div class="bg-option" @click="restoreDefaultBackground">
                  <i class="fas fa-undo"></i> {{ $t("baseChat.restoreBg") }}
                </div>
                <!-- 颜色选择器 -->
                <div class="color-picker-container" @click.stop>
                  <div
                    class="color-preview"
                    :style="{ background: selectedColor }"
                  ></div>
                  {{ $t("baseChat.customColor") }}
                  <input
                    type="color"
                    v-model="selectedColor"
                    @input.stop="setSolidBackground(selectedColor)"
                    class="color-picker"
                  />
                </div>
              </div>
            </transition>

            <button
              class="collapse-btn"
              @click="sessionCollapsed = !sessionCollapsed"
            >
              <i class="fas fa-chevron-left"></i>
            </button>
          </div>
          <div class="sessions-list-container">
            <div class="sessions-list">
              <div
                v-for="(session, idx) in sessions"
                :key="session.id"
                class="session-item"
                :class="{ active: idx === activeSessionIndex }"
                @click="switchToSession(idx)"
              >
                <div>
                  {{ $t("baseChat.session") }} {{ idx + 1 }}:
                  {{
                    session.messages[
                      session.messages.length - 1
                    ]?.content?.slice(0, 20)
                  }}
                </div>
                <div class="session-time">
                  {{ session.startTime.toLocaleTimeString() }}
                </div>
                <button
                  class="delete-session-btn"
                  @click.stop="clearSession(idx)"
                >
                  <i class="fas fa-trash-alt"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <div class="righttop-container">
      <slot name="righttop"></slot>
      <button
        v-if="showGuideButton"
        class="anime-btn"
        @click="showGuide = true"
      >
        <i class="fas fa-question"></i>
      </button>
    </div>
    <h1>{{ chatTitle }}</h1>
    <div class="leftbottom-container"></div>
    <div class="chat-container">
      <ThinkingIndicator
        :show="isThinking && mode !== 'smart-parallel'"
        :avatar="avatarPaths[currentAvatarIndex]"
        :time="thinkingTime"
      />
      <div
        class="chat-history"
        ref="chatHistoryRef"
        @scroll="onChatHistoryScroll"
      >
        <template
          v-for="(msg, idx) in sessions[activeSessionIndex]?.messages"
          :key="idx"
        >
          <!-- 用户消息 -->
          <div
            v-if="msg.sender === 'user'"
            class="message user-message fade-in"
          >
            <!-- 将文件显示移到内容上方 -->
            <div v-if="msg.files?.length" class="attached-files">
              <div
                v-for="(file, fIdx) in msg.files"
                :key="fIdx"
                class="file-tag"
              >
                <i :class="file.icon"></i>
                {{ file.name }}
              </div>
            </div>

            <!-- 文本内容 -->
            <div class="user-message-content" style="white-space: pre-wrap">
              {{ msg.content }}
            </div>
          </div>

          <!-- 智能体消息 -->
          <div v-else>
            <!-- 智能体并行模式特殊处理 -->
            <div
              v-if="mode === 'smart-parallel'"
              class="parallel-agent-message fade-in"
            >
              <div class="agent-header" @click="toggleMessageExpand(msg)">
                <img :src="msg.avatar" class="agent-avatar" />
                <span class="agent-name">{{ msg.agentName }}</span>
                <button class="expand-btn">
                  <i
                    :class="
                      msg.isExpanded
                        ? 'fas fa-chevron-down'
                        : 'fas fa-chevron-right'
                    "
                  ></i>
                </button>
              </div>
              <div
                v-if="msg.isExpanded"
                class="agent-message-bubble stream-container"
              >
                <div
                  class="stream-content"
                  v-html="
                    msg.rawContent ? marked.parse(msg.rawContent) : msg.html
                  "
                ></div>
                <div
                  v-if="hasCodeBlocks(msg.content)"
                  class="code-copy-container"
                  v-for="(code, index) in getCodeBlocks(msg.content)"
                  :key="index"
                >
                  <pre><code>{{ code }}</code></pre>
                  <button
                    class="copy-btn"
                    @click="copyToClipboard(code)"
                    title="复制代码"
                  >
                    <i class="fas fa-copy"></i>
                  </button>
                </div>
                <div class="translation-container">
                  <div
                    v-if="msg.translation && msg.showTranslation"
                    class="translation-content"
                  >
                    <div class="translation-text">{{ msg.translation }}</div>
                  </div>
                  <button
                    class="translate-btn"
                    v-if="msg.finished"
                    @click="translateMessage(msg)"
                    :disabled="msg.translating"
                  >
                    <div
                      class="fox-icon"
                      :class="{
                        thinking: msg.translating,
                        active: msg.translation && msg.showTranslation,
                      }"
                    >
                      <div class="fox-ears">
                        <div class="ear left"></div>
                        <div class="ear right"></div>
                      </div>
                      <div class="fox-face">
                        <div class="eyes">
                          <div class="eye left"></div>
                          <div class="eye right"></div>
                        </div>
                        <div class="nose"></div>
                      </div>
                    </div>
                  </button>
                </div>
              </div>
            </div>

            <!-- 其他模式保持原样 -->
            <div v-else class="agent-message-with-avatar fade-in">
              <img :src="msg.avatar || avatarPaths[0]" class="agent-avatar" />
              <div class="agent-info">
                <div class="agent-message-bubble stream-container">
                  <div
                    class="stream-content"
                    v-html="
                      msg.rawContent ? marked.parse(msg.rawContent) : msg.html
                    "
                  ></div>
                  <div
                    v-if="hasCodeBlocks(msg.content)"
                    class="code-copy-container"
                    v-for="(code, index) in getCodeBlocks(msg.content)"
                    :key="index"
                  >
                    <pre><code>{{ code }}</code></pre>
                    <button
                      class="copy-btn"
                      @click="copyToClipboard(code)"
                      title="复制代码"
                    >
                      <i class="fas fa-copy"></i>
                    </button>
                  </div>
                  <div class="translation-container">
                    <div
                      v-if="msg.translation && msg.showTranslation"
                      class="translation-content"
                    >
                      <div class="translation-text">{{ msg.translation }}</div>
                    </div>
                    <button
                      class="translate-btn"
                      v-if="msg.finished"
                      @click="translateMessage(msg)"
                      :disabled="msg.translating"
                    >
                      <div
                        class="fox-icon"
                        :class="{
                          thinking: msg.translating,
                          active: msg.translation && msg.showTranslation,
                        }"
                      >
                        <div class="fox-ears">
                          <div class="ear left"></div>
                          <div class="ear right"></div>
                        </div>
                        <div class="fox-face">
                          <div class="eyes">
                            <div class="eye left"></div>
                            <div class="eye right"></div>
                          </div>
                          <div class="nose"></div>
                        </div>
                      </div>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>
      <!-- 文件预览区域 -->
      <div class="file-previews" v-if="files.length > 0">
        <div
          v-for="(file, index) in files"
          :key="index"
          class="file-card"
          :class="{ expanded: file.isExpanded }"
        >
          <div class="card-header">
            <i :class="file.icon"></i>
            <div class="file-meta">
              <span class="file-name">{{ file.name }}</span>
              <span class="file-size">{{ formatFileSize(file.size) }}</span>
            </div>
            <div class="file-actions">
              <button
                class="action-btn view-btn"
                @click.stop="viewOriginal(file)"
              >
                <i class="fas fa-eye"></i>
              </button>
              <button
                class="action-btn edit-btn"
                @click.stop="editContent(file, index)"
              >
                <i class="fas fa-edit"></i>
              </button>
              <button
                class="action-btn delete-btn"
                @click.stop="removeFile(index)"
              >
                <i class="fas fa-times"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
      <!-- 输入区域 -->
      <div class="input-area">
        <textarea
          id="text-input-field"
          v-model="inputText"
          placeholder="请输入..."
          @keypress.enter.prevent="sendMessage"
          :disabled="isThinking"
        ></textarea>

        <div class="input-tools">
          <input
            type="file"
            class="tool-btn"
            style="display: none"
            ref="fileInput"
            @change="handleFileUpload"
            multiple
            accept="*/*"
          />
          <button
            class="tool-btn"
            @click="$refs.fileInput.click()"
            :disabled="isThinking"
          >
            <i class="fas fa-file-upload"></i>
          </button>
          <button
            class="tool-btn"
            v-if="
              selectedAgents.length < 2 ||
              (selectedAgents.length >= 2 && isDiscussionRunning)
            "
            @click="handleSendOrPause"
          >
            <i v-if="isThinking" class="fas fa-pause"></i>
            <i
              v-else-if="selectedAgents.length >= 2"
              class="fas fa-comments"
            ></i>
            <i v-else class="fas fa-paper-plane"></i>
          </button>
          <div v-if="selectedAgents.length >= 2" class="discussion-controls">
            <div
              v-if="selectedAgents.length >= 2 && !isDiscussionRunning"
              class="discussion-controls"
            >
              <button class="tool-btn" @click="toggleDiscussion">
                <i v-if="isDiscussionPaused" class="fas fa-play"></i>
                <i v-else class="fas fa-comments"></i>
              </button>
            </div>
            <button
              v-if="isDiscussionRunning"
              class="tool-btn stop-btn"
              @click="stopDiscussion"
            >
              <i class="fas fa-stop"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import {
  ref,
  reactive,
  inject,
  nextTick,
  watch,
  onMounted,
  computed,
  onBeforeUnmount,
} from "vue";
import { useI18n } from "vue-i18n";
const { t } = useI18n();
import ThinkingIndicator from "../Extension/ThinkingIndicator.vue";
import GuideModal from "../Extension/GuideModal.vue";
import { marked } from "marked";
import * as mammoth from "mammoth"; // DOCX处理库
import PptxReader from "pptxgenjs"; // PPTX处理库（示例）
import * as pdfjsLib from "pdfjs-dist/build/pdf";
import pdfjsWorker from "pdfjs-dist/build/pdf.worker?url";
pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorker;
import Tesseract from "tesseract.js";

const API_URL = "https://ds.1343263.xyz/api/process";
const isPaused = ref(false);
const abortController = ref(null); // 用于中断请求
const cachedResponse = ref(""); // 缓存已接收的响应内容
const sessionCollapsed = ref(true);
const showGuide = ref(false);
const showGuideButton = computed(() => {
  return !["group-discussion", "zero", "smart-parallel"].includes(props.mode);
});
const discussionLoop = ref(null); // 存储循环的引用
const isDiscussionRunning = ref(false); // 讨论是否正在进行
const isDiscussionPaused = ref(false); // 讨论是否暂停
const currentAgentIndex = ref(0); // 当前发言的agent索引
const props = defineProps({
  chatId: String,
  chatTitle: String,
  defaultBg: {
    type: String,
    required: true,
  },
  avatarPath: {
    type: String,
    required: true,
  },
  mode: String,
  selectedAgents: {
    type: Array,
    default: () => [],
  },
});
function getAgentName0(agentMode) {
  // 在selectedAgents中查找对应的agent对象
  const agent = props.selectedAgents.find((a) => a.mode === agentMode);
  // 如果找到则返回名字，否则返回默认的mode
  return agent ? agent.name : agentMode;
}
function getDisplayName(agentMode) {
  const agent = props.selectedAgents.find((a) => a.mode === agentMode);
  return agent ? agent.name : agentMode;
}
const showBgOptions = ref(false);
const selectedColor = ref("#ffffff");
const setSolidBackground = (color) => {
  // 先清理旧背景
  if (chatBg.value.startsWith("blob:")) {
    URL.revokeObjectURL(chatBg.value);
  }

  // 更新背景样式
  document.getElementById(props.chatId).style.backgroundImage = "none";
  document.getElementById(props.chatId).style.backgroundColor = color;

  // 存储到本地
  localStorage.setItem(`${props.chatId}-bg-type`, "color");
  localStorage.setItem(`${props.chatId}-bg`, color);
  chatBg.value = color;
  showBgOptions.value = false;
};

// 关闭菜单的逻辑
const closeBgMenu = (e) => {
  const menu = document.querySelector(".bg-options-menu");
  const colorPicker = document.querySelector(".color-picker-container");
  const isColorPickerInput = e.target.closest('input[type="color"]');

  if (
    menu &&
    !menu.contains(e.target) &&
    colorPicker &&
    !colorPicker.contains(e.target) &&
    !isColorPickerInput
  ) {
    showBgOptions.value = false;
  }
};
onMounted(() => {
  document.addEventListener("click", closeBgMenu);
});
onMounted(() => {
  // 新增：恢复会话滚动位置
  const savedScroll = sessionStorage.getItem("chatScrollPosition");
  if (savedScroll && chatHistoryRef.value) {
    chatHistoryRef.value.scrollTop = parseInt(savedScroll);
  }
});
onBeforeUnmount(() => {
  document.removeEventListener("click", closeBgMenu);
});
// 处理按钮点击（暂停/继续）
const handleSendOrPause = () => {
  if (
    isThinking.value ||
    (props.selectedAgents.length >= 2 && isDiscussionRunning.value)
  ) {
    pauseGeneration();
    if (props.selectedAgents.length >= 2) {
      isDiscussionPaused.value = true;
    }
  } else {
    sendMessage();
  }
};
function getAgentName(agentMode) {
  const agent = props.selectedAgents.find((a) => a.mode === agentMode);
  return agent ? agent.name : agentMode;
}

async function toggleMessageExpand(msg) {
  msg.isExpanded = !msg.isExpanded;
  await nextTick();
  scrollToBottom && scrollToBottom();
}
// 暂停生成
// 在 pauseGeneration 方法中添加缓存
const pauseGeneration = () => {
  isPaused.value = true;
  if (abortController.value) {
    // 直接中断请求，不保存缓存
    abortController.value.abort();
    abortController.value = null;

    // 找到未完成的Agent消息并标记为完成
    const session = sessions[activeSessionIndex.value];
    const lastMsg = session.messages.findLast(
      (m) => m.sender === "agent" && !m.finished
    );
    if (lastMsg) {
      lastMsg.finished = true;
      lastMsg.html = marked.parse(lastMsg.content);
    }
  }
  cachedResponse.value = "";
};
async function translateMessage(msg) {
  // 如果已有翻译，则切换显示/隐藏状态
  if (msg.translation) {
    msg.showTranslation = !msg.showTranslation;
    return;
  }

  msg.translating = true;
  msg.showTranslation = true; // 新增：设置初始显示状态

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        inputText: msg.content,
        agentMode: "only-translate",
        history: [],
      }),
    });

    if (!response.ok) throw new Error("翻译请求失败");

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let translation = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split("\n");

      for (const line of lines) {
        if (!line.trim()) continue;
        const data = JSON.parse(line);
        if (data.error) throw new Error(data.error);
        translation += data.content;
      }
    }

    msg.translation = translation;
  } catch (error) {
    showToast("翻译失败: " + error.message);
    msg.showTranslation = false;
  } finally {
    msg.translating = false;
  }
}
// 继续生成
const resumeGeneration = () => {
  isPaused.value = false;
  // 重新发送请求，携带已缓存的内容作为历史
  sendMessage(cachedResponse.value);
};
const emit = defineEmits(["back"]);
const showToast = inject("showToast");
const ocrWorker = ref(null);
const isOCRReady = ref(false);
const currentMode = ref(props.mode);
const avatarPaths = ref([props.avatarPath]);
const currentAvatarIndex = ref(0);
const files = ref([]);
const inputText = ref("");
const isThinking = ref(false);
const thinkingTime = ref("0.0s");
const thinkingTimer = ref(null);
const sessions = reactive([]);
const activeSessionIndex = ref(0);
const chatHistoryRef = ref(null);
const autoScroll = ref(true);
const fileInput = ref(null);
const showFileModal = ref(false);
const modalTitle = ref("");
const modalContent = ref("");
const editableContent = ref("");
const currentFileIndex = ref(-1);
const isImage = ref(false);
const chatBg = ref(props.defaultBg);
// 背景相关
const bgInput = ref(null);
const bgUrl = ref(props.defaultBg);
// 本地存储键名
const storageKey = computed(() => `${props.chatId}-sessions`);
// 加载本地会话
const loadSessions = () => {
  try {
    const saved = localStorage.getItem(storageKey.value);
    if (saved) {
      sessions.splice(
        0,
        sessions.length,
        ...JSON.parse(saved).map((s) => ({
          ...s,
          startTime: new Date(s.startTime),
          messages: s.messages.map((m) => ({
            ...m,
            // 恢复消息中的Date对象（如果需要）
            timestamp: m.timestamp ? new Date(m.timestamp) : new Date(),
          })),
        }))
      );
      activeSessionIndex.value = sessions.length > 0 ? 0 : -1;
    }
  } catch (e) {
    console.error("读取会话失败:", e);
  }
};

// 保存会话到本地存储
const saveSessions = () => {
  try {
    const toSave = sessions.map((s) => ({
      ...s,
      startTime: s.startTime.getTime(), // 转换为时间戳
      messages: s.messages.map((m) => ({
        ...m,
        // 转换Date对象为时间戳（如果需要）
        timestamp: m.timestamp?.getTime() || Date.now(),
      })),
    }));
    localStorage.setItem(storageKey.value, JSON.stringify(toSave));
  } catch (e) {
    console.error("保存会话失败:", e);
  }
};
const restoreDefaultBackground = () => {
  // 清除本地存储
  localStorage.removeItem(`${props.chatId}-bg`);
  // 恢复默认背景
  setBackground(props.defaultBg);
  showToast("已恢复默认背景");
};
const setBackground = (url) => {
  // 清除颜色背景
  document.getElementById(props.chatId).style.backgroundColor = "";

  // 设置图片背景
  if (chatBg.value.startsWith("blob:")) {
    URL.revokeObjectURL(chatBg.value);
  }
  chatBg.value = url;
  document.getElementById(props.chatId).style.backgroundImage = `url(${url})`;

  // 存储类型
  localStorage.setItem(`${props.chatId}-bg-type`, "image");
};

const toggleBackground = () => {
  bgInput.value.click(); // 使用ref直接触发点击
};

const setBackgroundFromInput = (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (event) => {
      const dataUrl = event.target.result;
      setBackground(dataUrl);
      localStorage.setItem(`${props.chatId}-bg`, dataUrl);
    };
    reader.readAsDataURL(file); // 读取为Base64
  }
};

// 释放URL对象
onBeforeUnmount(() => {
  if (chatBg.value.startsWith("blob:")) {
    URL.revokeObjectURL(chatBg.value);
  }
});
// 在组件卸载时停止讨论
onBeforeUnmount(() => {
  stopDiscussion();
});
// 确保背景初始化逻辑正确
onMounted(() => {
  const savedBgType = localStorage.getItem(`${props.chatId}-bg-type`);
  const savedBg = localStorage.getItem(`${props.chatId}-bg`);

  if (savedBg) {
    if (savedBgType === "color") {
      document.getElementById(props.chatId).style.backgroundColor = savedBg;
      document.getElementById(props.chatId).style.backgroundImage = "none";
    } else {
      setBackground(savedBg);
    }
  } else {
    setBackground(bgUrl.value);
  }
});

// 模态框关闭
const closeModal = () => {
  showFileModal.value = false;
  if (modalContent.value.startsWith("blob:")) {
    URL.revokeObjectURL(modalContent.value);
  }
};

// 查看原始文件
const viewOriginal = (file) => {
  const fileUrl = URL.createObjectURL(file.raw);
  const win = window.open(fileUrl, "_blank");
  setTimeout(() => {
    if (!win || win.closed) {
      showToast("请在浏览器设置中允许弹出窗口，或长按链接选择打开方式");
      const a = document.createElement("a");
      a.href = fileUrl;
      a.download = file.name;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
  }, 500);
  win?.addEventListener("beforeunload", () => {
    URL.revokeObjectURL(fileUrl);
  });
};
const processStreamContent = (content, existingContent) => {
  // 使用文本分块处理
  const chunkSize = 100;
  const chunks = [];
  for (let i = 0; i < content.length; i += chunkSize) {
    chunks.push(content.slice(i, i + chunkSize));
  }

  // 使用文档片段批量更新
  const fragment = document.createDocumentFragment();
  chunks.forEach((chunk) => {
    const span = document.createElement("span");
    span.textContent = chunk;
    fragment.appendChild(span);
  });

  return {
    safeContent: existingContent + content,
    buffer: "",
    hasPendingCode: false,
  };
};
// 编辑内容
const editContent = (file, index) => {
  editableContent.value = file.content;
  currentFileIndex.value = index;
  modalTitle.value = `编辑内容 - ${file.name}`;
  isImage.value = false;
  showFileModal.value = true;
};

// 保存更改
const saveChanges = () => {
  if (currentFileIndex.value >= 0) {
    files.value[currentFileIndex.value].content = editableContent.value;
    showFileModal.value = false;
    showToast("修改已保存");
  }
};

// 初始化OCR Worker
onMounted(async () => {
  await Tesseract.createWorker();
  isOCRReady.value = true;
});

onBeforeUnmount(async () => {
  if (ocrWorker.value) {
    await ocrWorker.value.terminate();
  }
});

// 生命周期钩子
onMounted(() => {
  if (chatHistoryRef.value) {
    chatHistoryRef.value.addEventListener("scroll", onChatHistoryScroll);
  }
  if (sessions.length === 0) createNewChat();
});

onBeforeUnmount(() => {
  if (chatHistoryRef.value) {
    chatHistoryRef.value.removeEventListener("scroll", onChatHistoryScroll);
  }
});

// 文件解析
const parseAnyFile = async (file, data) => {
  try {
    if (file.type.startsWith("image/")) {
      if (!isOCRReady.value) throw new Error("OCR引擎初始化中，请稍后");
      const {
        data: { text },
      } = await Tesseract.recognize(file);
      return text;
    }

    if (file.type === "application/pdf") {
      const loadingTask = pdfjsLib.getDocument({ data: new Uint8Array(data) });
      const pdf = await loadingTask.promise;
      let fullText = "";
      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const textContent = await page.getTextContent();
        fullText += textContent.items.map((item) => item.str).join("\n") + "\n";
      }
      return fullText;
    }

    if (file.name.endsWith(".docx")) {
      const result = await mammoth.extractRawText({ arrayBuffer: data });
      return result.value.replace(/\n{3,}/g, "\n\n");
    }

    if (file.name.endsWith(".pptx")) {
      const pptx = new PptxReader();
      await pptx.load(data);
      return pptx.slides
        .flatMap((slide) =>
          slide.shapes.filter((shape) => shape.text).map((shape) => shape.text)
        )
        .join("\n\n");
    }

    const encodings = [
      "utf-8",
      "gbk",
      "gb2312",
      "big5",
      "shift_jis",
      "windows-1252",
    ];
    let decodedText = "";
    for (const encoding of encodings) {
      try {
        const decoder = new TextDecoder(encoding, { fatal: true });
        decodedText = decoder.decode(new Uint8Array(data));
        if (!hasInvalidCharacters(decodedText)) {
          return decodedText;
        }
      } catch (e) {
        continue;
      }
    }
    return decodedText.replace(/[^\x00-\x7F]/g, "");
  } catch (e) {
    console.error("文件解析错误:", e);
    throw new Error(`文件解析失败: ${e.message}`);
  }
};

const hasInvalidCharacters = (text) => {
  return /[\x00-\x08\x0B-\x0C\x0E-\x1F]/.test(text);
};
const formatFileSize = (bytes) => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};

const handleFileUpload = async (e) => {
  const newFiles = Array.from(e.target.files);
  for (const file of newFiles) {
    try {
      const fileItem = {
        name: file.name,
        size: file.size,
        content: "",
        raw: file,
        icon: getFileIcon(file.name),
        progress: 0,
        status: "解析中...",
        isExpanded: false,
      };
      files.value.push(fileItem);

      const content = await readFileContent(file, (progress) => {
        fileItem.progress = Math.floor(progress * 100);
      });

      fileItem.content = content;
      fileItem.status = "解析完成";
      fileItem.progress = 100;
    } catch (error) {
      fileItem.status = `解析失败: ${error.message}`;
      fileItem.progress = 0;
      showToast(`${file.name} 处理失败: ${error.message}`);
    }
  }
  e.target.value = "";
};

const readFileContent = (file, onProgress) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    let lastLoaded = 0;

    reader.onprogress = (e) => {
      if (e.lengthComputable) {
        const progress = e.loaded / e.total;
        if (progress - lastLoaded > 0.05) {
          onProgress?.(progress);
          lastLoaded = progress;
        }
      }
    };

    reader.onload = async (e) => {
      try {
        const content = await parseAnyFile(file, e.target.result);
        resolve(content);
      } catch (error) {
        reject(error);
      }
    };

    reader.onerror = reject;
    reader.readAsArrayBuffer(file);
  });
};

const getFileIcon = (filename) => {
  const ext = filename.split(".").pop().toLowerCase();
  const icons = {
    pdf: "fa-file-pdf",
    jpg: "fa-file-image",
    png: "fa-file-image",
    doc: "fa-file-word",
    docx: "fa-file-word",
    ppt: "fa-file-powerpoint",
    pptx: "fa-file-powerpoint",
    txt: "fa-file-alt",
  };
  return `fas ${icons[ext] || "fa-file"}`;
};

const removeFile = (index) => {
  files.value.splice(index, 1);
};

// 会话管理
function createNewChat() {
  sessions.push({
    id: sessions.length,
    messages: [],
    startTime: new Date(),
    avatar: avatarPaths.value[currentAvatarIndex.value],
  });
  activeSessionIndex.value = sessions.length - 1;
  nextTick(scrollToBottom);
}

function switchToSession(idx) {
  activeSessionIndex.value = idx;
  nextTick(scrollToBottom);
}

// 代码块处理
function hasCodeBlocks(content) {
  return /```[\s\S]*?```/g.test(content);
}

function getCodeBlocks(content) {
  const matches = content.match(/```[\s\S]*?```/g);
  return matches
    ? matches.map((c) => c.replace(/```[\s\S]*?\n/, "").replace(/```$/, ""))
    : [];
}

async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    showToast("代码已复制到剪贴板！");
  } catch (err) {
    showToast("复制失败，请手动选择复制");
  }
}
async function handleOneMessage(cachedContent = "") {
  // 状态检查
  if (isPaused.value) {
    resumeGeneration();
    return;
  }

  // 获取当前会话
  const session = sessions[activeSessionIndex.value];

  // 构建完整对话历史（包含文件内容）
  const history = session.messages.flatMap((m) => {
    // 获取当前agent的显示名称
    const getAgentName = (mode) => {
      const agent = props.selectedAgents.find((a) => a.mode === mode);
      return agent ? agent.name : mode;
    };

    const baseEntry =
      m.sender === "user"
        ? {
            role: "user",
            content:
              m.content +
              (m.files?.length
                ? "\n[附件内容]\n" + m.files.map((f) => f.content).join("\n")
                : ""),
          }
        : {
            role: "assistant",
            content: m.content,
            name: getAgentName(m.agentMode),
          };

    // 只在多agent模式下保留完整对话，单agent只保留智能体消息
    return props.selectedAgents.length >= 2
      ? [baseEntry]
      : m.sender !== "user"
      ? [baseEntry]
      : [];
  });
  let combinedText = "";
  // 组合输入内容（包含历史对话）
  if (props.selectedAgents.length >= 2) {
    combinedText = history
      .map((entry) =>
        entry.role === "user"
          ? entry.content
          : `[${entry.name || getAgentName(currentMode.value)}] ${
              entry.content
            }`
      )
      .join("\n\n");
  } else {
    const textContent = inputText.value.trim();
    const fileContents = files.value.map((f) => f.content.trim()).join("\n\n");
    combinedText = [textContent, fileContents]
      .filter((t) => t.length > 0)
      .join("\n\n");
  }

  // 输入验证
  if (!combinedText.trim()) {
    showToast("请输入内容或上传文件");
    return;
  }

  // 只在第一个agent处理时添加用户消息
  if (!cachedContent && props.selectedAgents.length < 2) {
    session.messages.push({
      sender: "user",
      content: inputText.value,
      files: [...files.value],
    });
  }

  // 初始化请求控制
  abortController.value = new AbortController();
  isThinking.value = true;
  isPaused.value = false;
  let finalContent = cachedContent;

  // 思考指示器逻辑
  showThinkingIndicator();

  try {
    // API请求（携带完整对话历史）
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        inputText: combinedText,
        agentMode: currentMode.value,
        history: history,
        currentAgent: currentMode.value, // 告知后端当前处理agent
      }),
      signal: abortController.value.signal,
    });

    if (!response.ok) throw new Error(await response.text());

    // 流式处理（原有逻辑+缓存处理）
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    let firstOutput = true;
    let msg = null;
    let pendingCode = "";
    let isIncompleteCode = false;
    while (true) {
      if (isPaused.value) break; // 新增：暂停检查点

      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (!line.trim()) continue;
        const data = JSON.parse(line);
        if (data.error) throw new Error(data.error);
        // 处理代码块边界
        const processed = processStreamContent(data.content, pendingCode);
        const deltaContent = processed.safeContent;
        pendingCode = processed.buffer;
        isIncompleteCode = processed.hasPendingCode;
        // 消息初始化（原有代码）
        if (firstOutput) {
          msg = {
            sender: "agent",
            content: "", // 重置为空白内容
            html: '<span class="blinking-cursor">|</span>',
            avatar: avatarPaths.value[currentAvatarIndex.value],
            finished: false,
            agentMode: currentMode.value,
            agentName:
              props.selectedAgents.find((a) => a.mode === currentMode.value)
                ?.name || "",
            isExpanded: false,
          };
          session.messages.push(msg);
          firstOutput = false;
        }

        // 内容更新
        finalContent += deltaContent;
        cachedResponse.value = finalContent;
        msg.content = finalContent;
        // 仅当代码块闭合时才解析Markdown
        if (!isIncompleteCode) {
          msg.html =
            marked.parse(finalContent) +
            '<span class="blinking-cursor">|</span>';
          if (window.MathJax) {
            window.MathJax.Hub.Queue([
              "Typeset",
              window.MathJax.Hub,
              chatHistoryRef.value,
            ]);
          }
        } else {
          msg.html =
            marked.parse(finalContent + "```") +
            '<span class="blinking-cursor">|</span>' +
            '<div class="pending-code">代码生成中...</div>';
        }
        // 实时更新（原有代码）
        await nextTick();
        scrollToBottom();
        if (window.MathJax) {
          window.MathJax.Hub.Queue([
            "Typeset",
            window.MathJax.Hub,
            chatHistoryRef.value,
          ]);
        }
      }
    }

    // 最终处理（多agent模式特殊处理）
    if (msg) {
      if (typeof finalContent === "string") {
        msg.html = marked
          .parse(finalContent)
          .replace('<span class="blinking-cursor">|</span>', "");

        // 在多agent模式中存储独立内容
        msg.content = finalContent; // 仅存储当前agent的输出
        msg.rawContent = finalContent; // 新增独立存储字段
      }
      msg.time = thinkingTime.value;
      msg.finished = true;
    }
  } catch (e) {
    if (e.name !== "AbortError") {
    } else {
      console.log("请求已中止");
    }
  } finally {
    // 清理逻辑（多agent模式不立即清空）
    if (props.selectedAgents.length < 2) {
      inputText.value = "";
      files.value = [];
    }
    hideThinkingIndicator();
    isThinking.value = false;
    abortController.value = null;
    cachedResponse.value = "";

    await nextTick();
    isPaused.value = false; // 保持按钮状态不变
    if (window.MathJax) {
      window.MathJax.Hub.Queue([
        "Typeset",
        window.MathJax.Hub,
        chatHistoryRef.value,
      ]);
    }
  }
}
const toggleDiscussion = () => {
  if (isDiscussionRunning.value) {
    isDiscussionPaused.value = !isDiscussionPaused.value;
  } else {
    sendMessage();
  }
};

const stopDiscussion = () => {
  isDiscussionRunning.value = false;
  isDiscussionPaused.value = false;
  if (abortController.value) {
    abortController.value.abort();
  }
};
// 新增并行模式处理方法
async function handleOneMessageForAgent(
  agent,
  agentMsg,
  combinedText,
  session
) {
  // 构建历史记录
  const history = session.messages
    .filter((m) => m.sender !== "user")
    .map((m) => ({
      role: "assistant",
      content: m.content,
      name: m.agentName || agent.name,
    }));

  const controller = new AbortController();
  let finalContent = "";
  let buffer = "";
  let isIncompleteCode = false;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        inputText: combinedText,
        agentMode: agent.mode,
        history: history,
      }),
      signal: controller.signal,
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("API 响应错误:", {
        status: response.status,
        statusText: response.statusText,
        body: errorText,
      });
      throw new Error(
        `请求失败: ${response.status} - ${errorText || response.statusText}`
      );
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (!line.trim()) continue;

        try {
          const data = JSON.parse(line);
          if (data.error) throw new Error(data.error);

          const processed = processStreamContent(data.content, buffer);
          finalContent += processed.safeContent;
          buffer = processed.buffer;
          isIncompleteCode = processed.hasPendingCode;

          // 更新消息内容
          agentMsg.content = finalContent;
          agentMsg.html = isIncompleteCode
            ? marked.parse(finalContent + "```") +
              '<span class="blinking-cursor">|</span>' +
              '<div class="pending-code">代码生成中...</div>'
            : marked.parse(finalContent) +
              '<span class="blinking-cursor">|</span>';

          await nextTick();
          scrollToBottom();
        } catch (e) {
          console.error("解析响应错误:", e);
        }
      }
    }

    // 完成处理
    agentMsg.html = marked
      .parse(finalContent)
      .replace('<span class="blinking-cursor">|</span>', "");
    agentMsg.content = finalContent;
    agentMsg.rawContent = finalContent;
    agentMsg.finished = true;
  } catch (e) {
    console.error("智能体处理错误:", e);
    agentMsg.content = `请求失败: ${e.message}`;
    agentMsg.html = marked.parse(`**请求失败**: ${e.message}`);
    agentMsg.finished = true;
  }

  return agentMsg;
}

// 辅助方法：处理流式内容

// 消息发送逻辑
async function sendMessage() {
  if (!sessions[activeSessionIndex.value]) {
    createNewChat();
  }
  // 智能体并行模式特殊处理
  if (props.mode === "smart-parallel") {
    const session = sessions[activeSessionIndex.value];

    if (!props.selectedAgents || props.selectedAgents.length === 0) {
      showToast("请先选择智能体");
      return;
    }

    // 输入验证
    const textContent = inputText.value.trim();
    const fileContents = files.value.map((f) => f.content.trim()).join("\n\n");
    const combinedText = [textContent, fileContents]
      .filter((t) => t.length > 0)
      .join("\n\n");

    if (!combinedText) {
      showToast("请输入内容或上传文件");
      return;
    }

    // 添加用户消息
    session.messages.push({
      sender: "user",
      content: inputText.value,
      files: [...files.value],
      timestamp: new Date(),
    });

    // 为每个智能体创建初始消息
    const agentMessages = [];
    props.selectedAgents.forEach((agent) => {
      const agentMsg = {
        sender: "agent",
        content: "",
        html: '<span class="blinking-cursor">|</span>',
        avatar: agent.avatar, // 使用agent的头像
        agentMode: agent.mode, // agent的模式
        agentName: agent.name, // agent的名称
        finished: false,
        isExpanded: false, // 默认展开
        timestamp: new Date(),
        translating: false,
        translation: null,
        showTranslation: false,
      };
      session.messages.push(agentMsg);
      agentMessages.push({ agent, agentMsg });
    });

    // 清空输入
    inputText.value = "";
    files.value = [];

    // 滚动到底部
    nextTick(scrollToBottom);

    // 并行处理所有智能体的消息
    try {
      const requests = agentMessages.map(({ agent, agentMsg }) =>
        handleOneMessageForAgent(agent, agentMsg, combinedText, session)
      );
      await Promise.all(requests);
    } catch (error) {
      console.error("Parallel requests error:", error);
      showToast("部分智能体响应失败");
    }
    return;
  }
  if (props.selectedAgents.length >= 2) {
    const session = sessions[activeSessionIndex.value];
    // 先添加用户消息
    session.messages.push({
      sender: "user",
      content: inputText.value,
      files: [...files.value],
    });
    const runDiscussion = async () => {
      let accumulatedHistory = [...session.messages];
      isDiscussionRunning.value = true;

      while (isDiscussionRunning.value) {
        // 暂停状态等待
        if (isDiscussionPaused.value) {
          await new Promise((resolve) => setTimeout(resolve, 500));
          continue;
        }

        // 按顺序选择agent
        const agentMode = props.selectedAgents[currentAgentIndex.value];
        currentMode.value = agentMode;
        const newAvatar = new URL(
          `/src/assets/avatar/${currentMode.value}.jpg`,
          import.meta.url
        ).href;
        // 更新头像
        if (!avatarPaths.value.includes(newAvatar)) {
          avatarPaths.value = [newAvatar];
        }
        currentAvatarIndex.value = avatarPaths.value.indexOf(newAvatar);

        // 处理消息
        await handleOneMessage("", accumulatedHistory);

        // 更新历史和agent索引
        const lastMsg = session.messages[session.messages.length - 1];
        accumulatedHistory.push(lastMsg);
        currentAgentIndex.value =
          (currentAgentIndex.value + 1) % props.selectedAgents.length;

        // 添加短暂延迟使讨论更自然
        await new Promise((resolve) => setTimeout(resolve, 300));
      }
    };

    // 启动讨论
    discussionLoop.value = runDiscussion();
  } else {
    if (props.selectedAgents.length == 1) {
      currentMode.value = props.selectedAgents[0];
      const newAvatar = new URL(
        `/src/assets/avatar/${currentMode.value}.jpg`,
        import.meta.url
      ).href;

      // 更新头像
      if (!avatarPaths.value.includes(newAvatar)) {
        avatarPaths.value = [newAvatar];
      }
      currentAvatarIndex.value = avatarPaths.value.indexOf(newAvatar);
    }
    handleOneMessage();
  }

  // 清空输入
  inputText.value = "";
  files.value = [];
}

// 辅助函数
function showThinkingIndicator() {
  let start = Date.now();
  thinkingTime.value = "0.0s";
  thinkingTimer.value = setInterval(() => {
    thinkingTime.value = ((Date.now() - start) / 1000).toFixed(1) + "s";
  }, 100);
}

// 修改clearSession方法
function clearSession(idx) {
  // 先切换到其他会话
  if (sessions.length > 1) {
    activeSessionIndex.value = idx > 0 ? idx - 1 : 0;
  } else {
    createNewChat();
  }

  // 删除指定会话
  sessions.splice(idx, 1);

  // 如果删除的是当前会话且没有会话了，创建新会话
  if (sessions.length === 0) {
    createNewChat();
  }
  saveSessions();
}

function hideThinkingIndicator() {
  clearInterval(thinkingTimer.value);
  thinkingTime.value = "0.0s";
}

function onChatHistoryScroll() {
  const el = chatHistoryRef.value;
  if (!el) return;
  autoScroll.value = el.scrollHeight - el.scrollTop - el.clientHeight < 2;
  sessionStorage.setItem("chatScrollPosition", chatHistoryRef.value.scrollTop);
}

const scrollToBottom = () => {
  if (!chatHistoryRef.value || !autoScroll.value) return;

  const historyEl = chatHistoryRef.value;
  requestAnimationFrame(() => {
    historyEl.scrollTop = historyEl.scrollHeight;
  });
};
// 自动保存逻辑
watch(
  () => sessions,
  (newVal) => {
    saveSessions();
  },
  { deep: true }
);

// 组件挂载时加载会话
onMounted(() => {
  loadSessions();
  if (sessions.length === 0) {
    createNewChat();
  }
});
watch(
  () => sessions[activeSessionIndex.value]?.messages.length,
  async () => {
    await nextTick();
    if (window.MathJax && chatHistoryRef.value) {
      window.MathJax.Hub.Queue([
        "Typeset",
        window.MathJax.Hub,
        chatHistoryRef.value,
      ]);
    }
  }
);
defineExpose({
  isThinking,
  thinkingTime,
  sessions,
  activeSessionIndex,
  chatHistoryRef,
  files,
  inputText,
  handleFileUpload,
  removeFile,
  createNewChat,
  switchToSession,
  scrollToBottom,
  formatFileSize,
  getFileIcon,
  parseAnyFile,
  readFileContent,
  hasCodeBlocks,
  getCodeBlocks,
  copyToClipboard,
  onChatHistoryScroll,
  autoScroll,
});
</script>
<style scoped>
.color-picker-container {
  padding: 8px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.color-picker-container {
  /* 保持原有样式 */
  cursor: default; /* 防止点击穿透 */
  pointer-events: auto !important; /* 强制允许交互 */
}

.color-picker {
  /* 保持原有样式 */
  pointer-events: all; /* 允许颜色选择器交互 */
}
.color-picker {
  width: 30px;
  height: 30px;
  border: none;
  background: transparent;
  cursor: pointer;
}
.agent-message-bubble.stream-container.paused::after {
  content: "（已暂停）";
  color: #888;
  font-size: 0.9em;
  margin-left: 8px;
}
.color-picker::-webkit-color-swatch {
  border-radius: 50%;
  border: 2px solid #fff;
}

.color-picker::-moz-color-swatch {
  border-radius: 50%;
  border: 2px solid #fff;
}
.anime-btn[disabled] {
  opacity: 0.7;
  cursor: not-allowed;
}
.fa-pause,
.fa-play {
  margin: 0 2px;
}
.fa-comments {
  transform: rotateY(180deg); /* 镜像翻转图标 */
  margin-right: 2px;
}
.pending-code {
  color: #888;
  font-size: 0.9em;
  padding: 4px 0;
  border-left: 2px solid #4caf50;
  padding-left: 8px;
  margin-top: 4px;
}

.stream-content :deep(pre) {
  transition: opacity 0.3s ease;
}

.stream-content :deep(pre.pending) {
  opacity: 0.7;
  position: relative;
}

.stream-content :deep(pre.pending)::after {
  content: "代码加载中...";
  position: absolute;
  right: 10px;
  top: 5px;
  font-size: 0.8em;
  color: #666;
}
h1 {
  font-size: 1.6rem;
  margin-bottom: 0rem;
  color: #888; /* 灰色 */
  text-align: center;
  animation: none;
  position: relative;
  display: inline-block;
}
.chat-container {
  flex: 1;
  background-color: rgba(204, 252, 186, 0.1);
  border-radius: 10px;
  width: 900px;
  height: 100px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(103, 67, 67, 0.3);
  display: flex;
  flex-direction: column;
  position: relative;
}
.bg-options-menu {
  position: absolute;
  right: 40px;
  top: 40px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  padding: 8px 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 999;
  min-width: 160px;
}

.bg-option {
  padding: 8px 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #333;
  transition: all 0.2s;
}

.bg-option:hover {
  background: rgba(0, 0, 0, 0.05);
}

.color-preview {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: 1px solid #ddd;
}
.translation-container {
  position: relative;
  margin-top: 8px;
  border-top: 1px dashed rgba(255, 192, 203, 0.3); /* 使用粉色虚线 */
  padding-top: 8px;
}

.translate-btn {
  position: absolute;
  right: 4px;
  bottom: 2px;
  background: linear-gradient(
    135deg,
    #ffb7c5 0%,
    #ff69b4 100%
  ); /* 粉色渐变背景 */
  border: 2px solid #442ebf;
  color: white;
  cursor: pointer;
  padding: 6px;
  border-radius: 50%;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55); /* 弹性动画 */
  box-shadow: 0 2px 8px rgba(255, 105, 180, 0.3);
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9em;
}
.translate-btn {
  position: absolute;
  right: 4px;
  bottom: 2px;
  background: linear-gradient(135deg, #ffb7c5 0%, #ff69b4 100%);
  border: 2px solid #fff;
  cursor: pointer;
  padding: 6px;
  border-radius: 50%;
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  box-shadow: 0 2px 8px rgba(255, 105, 180, 0.3);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.fox-icon {
  width: 20px;
  height: 20px;
  position: relative;
}

.fox-ears {
  position: absolute;
  top: -8px;
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.ear {
  width: 0;
  height: 0;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-bottom: 8px solid #fff;
}

.ear.left {
  transform: rotate(-15deg);
}

.ear.right {
  transform: rotate(15deg);
}

.fox-face {
  width: 100%;
  height: 100%;
  background: #fff;
  border-radius: 50%;
  position: relative;
}

.eyes {
  position: absolute;
  top: 30%;
  width: 100%;
  display: flex;
  justify-content: space-around;
}

.eye {
  width: 3px;
  height: 3px;
  background: #ff69b4;
  border-radius: 50%;
}

.nose {
  position: absolute;
  bottom: 35%;
  left: 50%;
  transform: translateX(-50%);
  width: 4px;
  height: 4px;
  background: #ff69b4;
  border-radius: 50%;
}

/* 翻译中的动画效果 */
.fox-icon.thinking .eyes {
  animation: blink 1s infinite;
}

.fox-icon.thinking .ear {
  animation: earWiggle 1s infinite alternate;
}

@keyframes blink {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}

@keyframes earWiggle {
  0% {
    transform: rotate(-15deg);
  }
  100% {
    transform: rotate(15deg);
  }
}
.translation-content {
  font-size: 0.95em;
  color: #666;
  padding: 12px;
  background: rgba(255, 192, 203, 0.05);
  border-radius: 12px;
  margin-top: 8px;
  border: 1px solid rgba(255, 105, 180, 0.1);
  box-shadow: 0 2px 8px rgba(255, 192, 203, 0.1);
  animation: fadeInOut 0.3s ease;
}

.fox-icon.active {
  transform: rotate(180deg);
  transition: transform 0.3s ease;
}

@keyframes fadeInOut {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.translate-btn:hover .fox-face {
  transform: scale(1.1);
}

.translate-btn:hover .ear {
  border-bottom-color: #ffe4e1;
}

.translate-btn:disabled .fox-face {
  opacity: 0.7;
}

.translate-btn:disabled .ear {
  border-bottom-color: #ccc;
}

.translate-btn:disabled .eye,
.translate-btn:disabled .nose {
  background: #999;
}
.translate-btn:hover {
  transform: scale(1.1) rotate(5deg);
  background: linear-gradient(135deg, #ff69b4 0%, #ffb7c5 100%);
  box-shadow: 0 4px 12px rgba(255, 105, 180, 0.5);
}

.translate-btn:active {
  transform: scale(0.95);
}

.translate-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  background: linear-gradient(135deg, #ccc 0%, #999 100%);
  box-shadow: none;
}

.translate-btn i {
  animation: bounce 2s infinite;
}

.translation-content {
  font-size: 0.95em;
  color: #666;
  padding: 12px;
  background: rgba(255, 192, 203, 0.05);
  border-radius: 12px;
  margin-top: 8px;
  border: 1px solid rgba(255, 105, 180, 0.1);
  box-shadow: 0 2px 8px rgba(255, 192, 203, 0.1);
}

.translation-text {
  white-space: pre-wrap;
  line-height: 1.5;
}

/* 添加跳动动画 */
@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-2px);
  }
}

/* 添加翻译加载动画 */
.translate-btn .fa-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
@media (max-width: 768px) {
  .chat-container {
    width: 350px;
    height: 100px;
  }
  #text-input-field {
    flex: 1;
    padding: 10px 10px;
    border-radius: 20px;
    border: none;
    font-size: 1rem;
    background-color: rgba(242, 244, 227, 0.9);
    resize: none;
    height: 10px;
  }
  .file-previews {
    margin: 5px 0;
    width: 328px;
    max-height: 80px;
    overflow-y: auto;
    background: rgba(196, 233, 216, 0.8);
    border-radius: 10px;
    padding: 8px;
    box-shadow: 0 0 15px rgba(255, 192, 203, 0.5);
    border: 1px solid rgba(255, 192, 203, 0.3);
    position: absolute;
    bottom: 70px;
  }
  .input-area {
    display: flex;
    gap: 10px;
    padding: 15px;
    background-color: rgba(182, 109, 109, 0.1);
    position: absolute;
    bottom: 0px;
    width: 330px;
  }
  .file-card {
    flex: 0 0 200px;
    background: rgb(136, 102, 102);
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    cursor: pointer;
    overflow: hidden;
    max-width: 170px;
  }
  .user-message-content {
    background-color: rgba(50, 223, 223, 0.8);
    padding: 10px 10px;
    border-radius: 10px;
    font-size: 1rem;
    line-height: 1.1;
    color: #000000;
    word-break: break-word;
    white-space: pre-wrap;
  }
}
/* 会话列表头部 */
.sessions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1px;
  background: #dcd6cb;
  border-radius: 10px;
  box-shadow: 0 6px 20px rgba(103, 30, 135, 0.08);
  padding: 10px 16px 10px 16px;
  z-index: 10;
  transition: background 0.3s, box-shadow 0.2s;
}

.sessions-header:active {
  background: #dcd6cb;
  box-shadow: 0 2px 5px rgba(142, 68, 173, 0.08);
}

.sessions-header.selected,
.sessions-header:focus,
.sessions-header:hover {
  background: #edeae4;
  box-shadow: 0 12px 25px rgba(205, 176, 218, 0.12);
}

.sessions-header h3 {
  margin: 0;
  font-size: 20px;
  margin-left: 0px;
  color: #ed488d;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}
.discussion-controls {
  display: flex;
  gap: 5px;
}

.stop-btn {
  color: #ff4d4d;
}
/* 会话列表容器 */
.sessions-list-container {
  height: calc(100% - 60px); /* 减去标题栏高度 */
  overflow-y: auto;
  padding: 1px;
  background: linear-gradient(
    145deg,
    rgba(201, 23, 23, 0.05),
    rgba(255, 255, 255, 0.15)
  );

  border-radius: 15px;
}

.sessions-list-container::-webkit-scrollbar {
  width: 6px;
}

.sessions-list-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.sessions-list-container::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 10px;
}

.sessions-list-container::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

.session-item {
  padding: 1px;
  margin-bottom: 1.5px;
  background: linear-gradient(
    145deg,
    rgba(255, 255, 255, 0.1),
    rgba(255, 255, 255, 0.2)
  );
  background-color: #deeec5;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.session-item:hover {
  background: linear-gradient(
    145deg,
    rgba(15, 99, 173, 0.2),
    rgba(162, 210, 31, 0.3)
  );
  transform: translateY(-2px);
}

.session-item.active {
  background: linear-gradient(
    145deg,
    rgba(170, 255, 204, 0.2),
    rgba(170, 255, 204, 0.4)
  );
  border-left: 3px solid #ee2e81;
  box-shadow: 0 6px 15px rgba(170, 255, 204, 0.3);
}

.session-item .session-title {
  font-size: 1rem;
  color: #333;
  margin-bottom: 5px;
  text-shadow: none;
}

.session-time {
  font-size: 0.8rem;
  color: rgba(151, 7, 115, 0.7);
  margin-top: 5px;
}

.delete-session-btn {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: transparent;
  border: none;
  color: #3207b6;
  font-size: 1rem;
  cursor: pointer;
  opacity: 0.7;
  z-index: 2;
  padding: 2px 4px;
  transition: color 0.2s, opacity 0.2s;
}

.delete-session-btn:hover {
  color: #ff0000;
  opacity: 1;
}

.session-item {
  transition: all 0.01s ease;
  overflow: hidden;
}

/* 删除时动画 */
.session-item-leave-active {
  transition: all 0.3s;
  max-height: 0;
  opacity: 0;
  margin-bottom: 0;
  padding: 0;
}
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform, opacity;
}

.slide-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.slide-enter-to {
  opacity: 1;
  transform: translateX(0);
}

.slide-leave-from {
  opacity: 1;
  transform: translateX(0);
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

/* 调整折叠按钮位置 */
.sessions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 10px;
}
.session-sidebar {
  position: absolute;
  left: 10px; /* 让它不遮住展开按钮 */
  top: 48px; /* 与 .lefttop-second-container 对齐 */
  width: 228px;
  border-radius: 8px;
  overflow: hidden;
  z-index: 9;
  max-height: 580px;
  height: calc(100vh - 100px); /* 动态高度适配屏幕 */
}
.parallel-agent-message {
  background: rgba(120, 223, 154, 0.95);
  border-radius: 18px;
  margin: 15px 10px;
  border: 2px solid rgba(223, 205, 208, 0.5);
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.parallel-agent-message:hover {
  transform: translateY(-2px);
}

.parallel-agent-message::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;

  opacity: 0.7;
}

.agent-header {
  padding: 12px 15px;
  display: flex;
  align-items: center;
  cursor: pointer;
  background: rgba(0, 0, 0, 0.2);
}

.agent-name {
  flex: 1;
  margin-left: 10px;
  font-weight: 500;
  color: #ffd700;
}

.agent-content {
  padding: 15px;
  background: rgba(0, 0, 0, 0.1);
}
.agent-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.agent-info .agent-name {
  font-size: 0.9em;
  color: #ffd700;
  margin-bottom: 4px;
  margin-left: 8px;
}

.agent-message-with-avatar {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
  position: relative;
}
</style>
