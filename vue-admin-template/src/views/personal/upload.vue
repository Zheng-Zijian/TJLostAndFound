<template>
  <div class="app-container">
    <h2 class="title" style="text-align: center;">您上传的失物列表</h2>
    <el-form :inline="true">
      <el-form-item label="物品:">
        <el-input v-model="search" placeholder="搜索失物..." class="input" @keydown.enter.native="handleSearch" />
      </el-form-item>
      <el-form-item label="类别:">
        <el-select v-model="category" placeholder="请选择类别" @change="fetchItems">
          <el-option value="" label="所有类别" />
          <el-option value="雨伞" label="雨伞" />
          <el-option value="眼镜" label="眼镜" />
          <el-option value="3C电子" label="3C电子" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态:">
        <el-select v-model="claimedStatus" placeholder="请选择状态" @change="fetchItems">
          <el-option value="" label="全部" />
          <el-option value="claimed" label="已认领" />
          <el-option value="unclaimed" label="未认领" />
        </el-select>
      </el-form-item>
      <el-button type="primary" @click="AddItem">上传失物</el-button>
    </el-form>
    <el-table v-loading="listLoading" :data="items" element-loading-text="Loading" border fit highlight-current-row
      :default-sort="{ prop: 'time', order: 'descending' }">
      <el-table-column align="center" label="编号" width="95">
        <template slot-scope="scope">
          #{{ scope.row.id }}
        </template>
      </el-table-column>
      <el-table-column label="物品名称" align="center">
        <template slot-scope="scope">
          {{ scope.row.item_name }}
        </template>
      </el-table-column>
      <el-table-column label="类别" align="center">
        <template slot-scope="scope" align="center">
          <span>{{ scope.row.category }}</span>
        </template>
      </el-table-column>
      <el-table-column label="拾得地点" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.location }}
        </template>
      </el-table-column>
      <el-table-column align="center" prop="time" label="拾得时间" sortable>
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.found_date }}</span>
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="状态" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.claimed | statusFilter">{{ scope.row.claimed ? '已认领' : '未认领' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="认领用户" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.claimed_user || '--' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="详情" align="center">
        <template slot-scope="scope">
          <el-popover placement="top" title="物品描述" width="200">
            <p>{{ scope.row.description }}</p>
            <el-button slot="reference" type="text">详情</el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="210">
        <template slot-scope="scope">
          <el-button type="primary" size="small" style="margin-right: 10px"
            @click="ConfirmClaimStatus(scope.row.id, scope.row.item_name, scope.row.category, scope.row.claimed)">
            确认认领
          </el-button>
          <el-button type="danger" size="small"
            @click="DeleteItem(scope.row.id, scope.row.item_name, scope.row.category, scope.row.claimed, scope.row.claimed_user)">
            删除失物
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :visible.sync="add_modalVisible" title="上传失物" @close="closeAddModal(false)">
      <p style="display: flex; align-items: center; margin-bottom: 15px;">
        <strong style="margin-right: 10px; white-space: nowrap;">失物名称:</strong>
        <el-input v-model="upload_item_name" placeholder="请输入失物名称..." style="flex: 1;" />
      </p>
      <p style="display: flex; align-items: center; margin-bottom: 15px;">
        <strong style="margin-right: 10px; white-space: nowrap;">失物类别:</strong>
        <el-select v-model="upload_item_category" placeholder="请选择失物类别..." style="flex: 1;">
          <el-option value="雨伞" label="雨伞" />
          <el-option value="眼镜" label="眼镜" />
          <el-option value="3C电子" label="3C电子" />
        </el-select>
      </p>
      <p style="display: flex; align-items: center; margin-bottom: 15px;">
        <strong style="margin-right: 10px; white-space: nowrap;">拾得地点:</strong>
        <el-input v-model="upload_item_location" placeholder="请输入拾得地点..." style="flex: 1;" />
      </p>
      <p style="display: flex; align-items: center; margin-bottom: 15px;">
        <strong style="margin-right: 10px; white-space: nowrap;">拾得时间:</strong>
        <el-date-picker v-model="upload_item_time" type="date" value-format="yyyy-MM-dd" placeholder="请选择拾得时间..."
          style="flex: 1;" />
      </p>
      <p style="display: flex; align-items: center; margin-bottom: 15px;">
        <strong style="margin-right: 10px; white-space: nowrap;">描述信息:</strong>
        <el-input v-model="upload_item_description" placeholder="请输入额外描述信息..." style="flex: 1;" />
      </p>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="closeAddModal(true)">确 认</el-button>
        <el-button @click="closeAddModal(false)">取 消</el-button>
      </span>
    </el-dialog>

    <el-dialog :visible.sync="confirm_modalVisible" title="确认认领状态" @close="closeConfirmModal(false)">
      <p><strong>失物编号:</strong>{{ claim_item_id }}</p>
      <p><strong>失物名称:</strong>{{ claim_item_name }}</p>
      <p><strong>失物类别:</strong>{{ claim_item_category }}</p>
      <p><strong>认领状态:</strong>{{ claim_item_claimed }}</p>
      <el-input v-model="nowclaimed_user" placeholder="认领用户..." class="input" />
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="closeConfirmModal(true)">确 认</el-button>
        <el-button type="primary" @click="closeConfirmModal(false)">取 消</el-button>
      </span>
    </el-dialog>

    <el-dialog :visible.sync="delete_modalVisible" title="是否删除失物信息?" @close="closeDeleteModal(false)">
      <p><strong>失物编号:</strong>{{ delete_item_id }}</p>
      <p><strong>失物名称:</strong>{{ delete_item_name }}</p>
      <p><strong>失物类别:</strong>{{ delete_item_category }}</p>
      <p><strong>认领状态:</strong>{{ delete_item_claimed }}</p>
      <p><strong>认领用户:</strong>{{ delete_item_claimed_user }}</p>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="closeDeleteModal(true)">确 认</el-button>
        <el-button type="primary" @click="closeDeleteModal(false)">取 消</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
import { getItems } from '@/api/table'
import { getInfo } from '@/api/user'
import { getUserContactInfo } from '@/api/user'
import { addItem } from '@/api/table'
import { deleteItem } from '@/api/table'
import { claimItem } from '@/api/request'
import _ from 'lodash'
import { Message } from 'element-ui'
export default {
  filters: {
    statusFilter(status) {
      if (status) {
        return 'success'
      }
      return ''
    }
  },
  data() {
    return {
      results: [],
      listLoading: true,
      items: [],
      category: '',
      search: '',
      claimedStatus: '',
      tooltipVisible: false,
      tooltipContent: '',
      tooltipStyle: {},
      modalVisible: false,
      add_modalVisible: false,
      confirm_modalVisible: false,
      delete_modalVisible: false,
      modalUser: '',
      modalContact: '',
      upload_user_Info: '',
      upload_item_name: '',
      upload_item_category: '',
      upload_item_location: '',
      upload_item_time: '',
      upload_item_description: '',
      upload_user_contact_info: '',
      claim_item_id: '',
      claim_item_name: '',
      claim_item_category: '',
      claim_item_claimed: '',
      claim_item_description: '',
      nowclaimed_user: '',
      delete_item_id: '',
      delete_item_name: '',
      delete_item_category: '',
      delete_item_claimed: '',
      delete_item_claimed_user: '',
      delete_item_description: '',
      sortOrder: 'asc', // 排序方式，默认为升序
      userInfo: null
    }
  },
  mounted() {
    this.fetchUserInfo()
  },
  methods: {
    fetchUserInfo() {
      const token = localStorage.getItem('access_token')
      getInfo(token)
        .then(response => {
          this.userInfo = response.data
          this.fetchItems()
        })
        .catch(error => {
          console.error('获取用户信息失败:', error)
        })
    },

    fetchItems() {
      console.log('排序方式值值:', this.sortOrder)
      getItems({
        category: this.category,
        search: this.search.trim(),
        claimed: this.claimedStatus,
        sort: this.sortOrder,
        upload_user: this.userInfo.name
      }).then(response => {
        this.items = response.data
        this.listLoading = false
      })
        .catch(error => {
          console.error('获取失物列表失败:', error)
        })
    },
    // createFilter(queryString) {
    //   return (items) => {
    //     return _.includes(items.item_name, queryString);
    //   };
    // }
    handleSearch() {
      this.fetchItems()
      this.search = ''
    },
    showDescription(description) {
      this.tooltipVisible = true
      this.tooltipContent = description || '无描述'
    },
    hideDescription() {
      this.tooltipVisible = false
    },
    showContactInfo(user, contact) {
      this.modalUser = user
      this.modalContact = contact || '无'
      this.modalVisible = true
    },
    closeModal() {
      this.modalVisible = false
    },
    toggleSortOrder() {
      // 切换排序方式
      this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'
      this.fetchItems()
    },
    AddItem() {
      this.add_modalVisible = true
    },
    closeAddModal(confirmed) {
      this.add_modalVisible = false
      if (confirmed) {
        const token = localStorage.getItem('access_token')
        getUserContactInfo(token, this.userInfo.name)
          .then(reponse => {
            this.upload_user_Info = reponse.data
            this.upload_user_contact_info = this.upload_user_Info.contact_info.email
          })
          .catch(error => {
            console.error('获取用户联系方式失败:', error)
          })
        console.log(this.upload_user_contact_info)
        const data = {
          item_name: this.upload_item_name,
          category: this.upload_item_category,
          location: this.upload_item_location,
          found_date: this.upload_item_time,
          upload_user: this.userInfo.name,
          description: this.upload_item_description,
          contact_info: this.upload_user_contact_info
        }
        addItem(data)
          .then(() => {
            Message({
              type:'success',
              message: '上传成功'
            })
            this.fetchItems()
              .catch(error => {
                console.error('获取失物列表失败:', error)
              })
          })
          .catch(error => {
            console.error('上传失物失败:', error)
          })
      }
    },
    DeleteItem(id, name, category, claimed, claimed_user) {
      this.delete_modalVisible = true
      this.delete_item_id = id
      this.delete_item_name = name
      this.delete_item_category = category
      this.delete_item_claimed = claimed ? '已认领' : '未认领'
      this.delete_item_claimed_user = claimed_user || '无'
    },
    closeDeleteModal(confirmed) {
      this.delete_modalVisible = false
      if (confirmed) {
        deleteItem(this.delete_item_id)
          .then(() => {
            Message({
              type: 'success',
              message: '删除成功'
            })
            this.fetchItems()
              .catch(error => {
                console.error('获取失物列表失败:', error)
              })
          })
          .catch(error => {
            console.error('删除失物失败:', error)
          })
      }
    },
    ConfirmClaimStatus(id, name, category, claimed) {
      this.confirm_modalVisible = true
      this.claim_item_id = id
      this.claim_item_name = name
      this.claim_item_category = category
      this.claim_item_claimed = claimed ? '已认领' : '未认领'
    },
    closeConfirmModal(confirmed) {
      this.confirm_modalVisible = false // 关闭弹框
      if (confirmed) {
        // 构建请求体数据
        const data = {
          item_id: this.claim_item_id,
          claimed_user: this.nowclaimed_user // 确保传递 claimed_user
        }

        // 调用 claimItem 函数，传递 itemId 和 data
        claimItem(this.claim_item_id, data).then(response => {
          // 成功时的逻辑
          Message({
            type: 'success',
            message: '认领成功'
          })
          this.fetchItems()
          console.log('Item claimed successfully:', response)
          // 你可以在这里更新 UI 或做其他处理，比如刷新失物列表
        }).catch(error => {
          // 错误时的处理
          console.error('Failed to claim item:', error)
          // 你可以在这里显示错误提示
        })
      }
    }

  }
}
</script>
<style scoped>
/* 整体样式 */
</style>
