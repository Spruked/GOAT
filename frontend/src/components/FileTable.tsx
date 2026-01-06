import React, { useState, useMemo, useCallback } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  ColumnDef,
  SortingState,
  ColumnFiltersState,
  flexRender,
} from '@tanstack/react-table';
import { useInfiniteQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useInView } from 'react-intersection-observer';
import {
  ChevronUp,
  ChevronDown,
  Star,
  Download,
  Trash2,
  MoreHorizontal,
  CheckSquare,
  Square,
  FileText,
  Image,
  Film,
  File,
  AlertCircle,
  CheckCircle,
  Clock,
} from 'lucide-react';
import axios from 'axios';
import { formatBytes, statusColors, getFileIcon, getFileTypeFromMime } from '../../utils/file';
import { format } from 'date-fns';

interface UserFile {
  id: string;
  display_name: string;
  file_name: string;
  file_size: number;
  file_type: string;
  mime_type: string;
  status: 'uploaded' | 'processing' | 'processed' | 'failed';
  is_favorite: boolean;
  thumbnail_path?: string;
  created_at: string;
  updated_at: string;
}

interface FileTableProps {
  user: any;
}

export function FileTable({ user }: FileTableProps) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [rowSelection, setRowSelection] = useState({});
  const [globalFilter, setGlobalFilter] = useState('');
  const queryClient = useQueryClient();

  // Infinite query for files
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
    isError,
  } = useInfiniteQuery({
    queryKey: ['user-files-infinite', globalFilter, sorting, columnFilters],
    queryFn: async ({ pageParam = 0 }) => {
      const params = new URLSearchParams();
      params.append('page', pageParam.toString());
      params.append('limit', '50');

      // Add sorting
      if (sorting.length > 0) {
        params.append('sort_by', sorting[0].id);
        params.append('sort_order', sorting[0].desc ? 'desc' : 'asc');
      }

      // Add global filter
      if (globalFilter) {
        params.append('search', globalFilter);
      }

      // Add column filters
      columnFilters.forEach(filter => {
        if (filter.value) {
          params.append(`filter_${filter.id}`, filter.value as string);
        }
      });

      const { data } = await axios.get(`/api/user/files?${params}`);
      return data;
    },
    getNextPageParam: (lastPage) => lastPage.pagination?.has_more ? lastPage.pagination.page + 1 : undefined,
    initialPageParam: 0,
  });

  // Intersection observer for infinite scroll
  const { ref, inView } = useInView({
    threshold: 0,
    rootMargin: '100px',
  });

  React.useEffect(() => {
    if (inView && hasNextPage && !isFetchingNextPage) {
      fetchNextPage();
    }
  }, [inView, hasNextPage, isFetchingNextPage, fetchNextPage]);

  // Mutations
  const toggleFavoriteMutation = useMutation({
    mutationFn: async (fileId: string) => {
      const { data } = await axios.post(`/api/user/files/${fileId}/favorite`);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['user-files-infinite']);
    },
  });

  const deleteFileMutation = useMutation({
    mutationFn: async (fileId: string) => {
      await axios.delete(`/api/user/files/${fileId}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['user-files-infinite']);
      setRowSelection({});
    },
  });

  const bulkDeleteMutation = useMutation({
    mutationFn: async (fileIds: string[]) => {
      await Promise.all(fileIds.map(id => axios.delete(`/api/user/files/${id}`)));
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['user-files-infinite']);
      setRowSelection({});
    },
  });

  // Flatten the data
  const flatData = useMemo(() => {
    return data?.pages?.flatMap(page => page.files) ?? [];
  }, [data]);

  // Column definitions
  const columns = useMemo<ColumnDef<UserFile>[]>(() => [
    {
      id: 'select',
      header: ({ table }) => (
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={table.getIsAllRowsSelected()}
            onChange={table.getToggleAllRowsSelectedHandler()}
            className="rounded border-slate-600 bg-slate-700"
          />
        </div>
      ),
      cell: ({ row }) => (
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={row.getIsSelected()}
            onChange={row.getToggleSelectedHandler()}
            className="rounded border-slate-600 bg-slate-700"
          />
        </div>
      ),
      size: 40,
      enableSorting: false,
    },
    {
      accessorKey: 'is_favorite',
      header: '',
      cell: ({ row }) => (
        <button
          onClick={() => toggleFavoriteMutation.mutate(row.original.id)}
          className={`p-1 rounded hover:bg-slate-700 ${
            row.original.is_favorite ? 'text-yellow-400' : 'text-slate-400'
          }`}
        >
          <Star size={16} fill={row.original.is_favorite ? 'currentColor' : 'none'} />
        </button>
      ),
      size: 40,
      enableSorting: false,
    },
    {
      accessorKey: 'thumbnail_path',
      header: 'Preview',
      cell: ({ row }) => {
        const file = row.original;
        const IconComponent = getFileIconComponent(file.mime_type);

        return (
          <div className="w-12 h-12 flex items-center justify-center bg-slate-700 rounded">
            {file.thumbnail_path ? (
              <img
                src={file.thumbnail_path}
                alt={file.display_name}
                className="w-full h-full object-cover rounded"
              />
            ) : (
              <IconComponent size={24} className="text-slate-400" />
            )}
          </div>
        );
      },
      size: 60,
      enableSorting: false,
    },
    {
      accessorKey: 'display_name',
      header: 'Name',
      cell: ({ row }) => (
        <div className="max-w-xs">
          <div className="font-medium truncate" title={row.original.display_name}>
            {row.original.display_name}
          </div>
          <div className="text-sm text-slate-400 truncate" title={row.original.file_name}>
            {row.original.file_name}
          </div>
        </div>
      ),
      size: 200,
    },
    {
      accessorKey: 'status',
      header: 'Status',
      cell: ({ row }) => <StatusBadge status={row.original.status} />,
      size: 100,
    },
    {
      accessorKey: 'file_size',
      header: 'Size',
      cell: ({ row }) => (
        <span className="text-sm">{formatBytes(row.original.file_size)}</span>
      ),
      size: 80,
    },
    {
      accessorKey: 'created_at',
      header: 'Date Added',
      cell: ({ row }) => (
        <span className="text-sm text-slate-400">
          {format(new Date(row.original.created_at), 'MMM dd, yyyy')}
        </span>
      ),
      size: 120,
    },
    {
      id: 'actions',
      header: '',
      cell: ({ row }) => (
        <div className="flex items-center space-x-1">
          <button
            onClick={() => {
              // Download logic
              window.open(`/api/user/files/${row.original.id}/download`, '_blank');
            }}
            className="p-1 rounded hover:bg-slate-700 text-slate-400 hover:text-slate-300"
            title="Download"
          >
            <Download size={16} />
          </button>
          <button
            onClick={() => {
              if (confirm(`Delete "${row.original.display_name}"?`)) {
                deleteFileMutation.mutate(row.original.id);
              }
            }}
            className="p-1 rounded hover:bg-slate-700 text-slate-400 hover:text-red-400"
            title="Delete"
          >
            <Trash2 size={16} />
          </button>
        </div>
      ),
      size: 80,
      enableSorting: false,
    },
  ], [toggleFavoriteMutation, deleteFileMutation]);

  const table = useReactTable({
    data: flatData,
    columns,
    state: {
      sorting,
      columnFilters,
      globalFilter,
      rowSelection,
    },
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onGlobalFilterChange: setGlobalFilter,
    onRowSelectionChange: setRowSelection,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    enableRowSelection: true,
  });

  const selectedRows = table.getSelectedRowModel().rows;
  const selectedFileIds = selectedRows.map(row => row.original.id);

  const handleBulkDelete = () => {
    if (selectedFileIds.length > 0 && confirm(`Delete ${selectedFileIds.length} selected files?`)) {
      bulkDeleteMutation.mutate(selectedFileIds);
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-4">
        <div className="h-10 bg-slate-700 rounded animate-pulse"></div>
        {[...Array(10)].map((_, i) => (
          <div key={i} className="h-16 bg-slate-700 rounded animate-pulse"></div>
        ))}
      </div>
    );
  }

  if (isError) {
    return (
      <div className="text-center py-20">
        <AlertCircle size={64} className="text-red-400 mx-auto mb-4" />
        <h3 className="text-xl font-medium mb-2">Failed to load files</h3>
        <p className="text-slate-400">Please try again later</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Search and Filters */}
      <div className="flex items-center justify-between">
        <div className="flex-1 max-w-md">
          <input
            type="text"
            placeholder="Search files..."
            value={globalFilter}
            onChange={(e) => setGlobalFilter(e.target.value)}
            className="w-full bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-goat-primary"
          />
        </div>
        {selectedRows.length > 0 && (
          <div className="flex items-center space-x-2">
            <span className="text-sm text-slate-400">
              {selectedRows.length} selected
            </span>
            <button
              onClick={handleBulkDelete}
              className="bg-red-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-red-700 transition-colors"
              disabled={bulkDeleteMutation.isPending}
            >
              <Trash2 size={16} className="mr-2" />
              Delete Selected
            </button>
          </div>
        )}
      </div>

      {/* Table */}
      <div className="goat-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-slate-800">
              {table.getHeaderGroups().map((headerGroup) => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map((header) => (
                    <th
                      key={header.id}
                      className="px-4 py-3 text-left text-xs font-medium text-slate-300 uppercase tracking-wider"
                      style={{ width: header.getSize() }}
                    >
                      {header.isPlaceholder ? null : (
                        <div
                          className={header.column.getCanSort() ? 'cursor-pointer select-none flex items-center' : ''}
                          onClick={header.column.getToggleSortingHandler()}
                        >
                          {flexRender(header.column.columnDef.header, header.getContext())}
                          {header.column.getCanSort() && (
                            <div className="ml-1">
                              {header.column.getIsSorted() === 'asc' && <ChevronUp size={14} />}
                              {header.column.getIsSorted() === 'desc' && <ChevronDown size={14} />}
                              {header.column.getIsSorted() === false && <div className="w-3.5 h-3.5" />}
                            </div>
                          )}
                        </div>
                      )}
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody className="divide-y divide-slate-700">
              {table.getRowModel().rows.map((row) => (
                <tr key={row.id} className="hover:bg-slate-700/50">
                  {row.getVisibleCells().map((cell) => (
                    <td key={cell.id} className="px-4 py-3">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Infinite scroll trigger */}
        <div ref={ref} className="p-4 text-center">
          {isFetchingNextPage ? (
            <div className="flex items-center justify-center space-x-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-goat-primary"></div>
              <span className="text-slate-400">Loading more files...</span>
            </div>
          ) : hasNextPage ? (
            <span className="text-slate-400">Scroll for more files</span>
          ) : (
            <span className="text-slate-400">No more files</span>
          )}
        </div>
      </div>
    </div>
  );
}

function getFileIconComponent(mimeType: string) {
  const type = getFileTypeFromMime(mimeType);
  switch (type) {
    case 'image':
      return Image;
    case 'video':
      return Film;
    case 'pdf':
      return FileText;
    default:
      return File;
  }
}

function StatusBadge({ status }: { status: string }) {
  const statusConfig = {
    uploaded: { color: 'bg-yellow-500/20 text-yellow-400', label: 'Uploaded', icon: Clock },
    processing: { color: 'bg-blue-500/20 text-blue-400', label: 'Processing', icon: Clock },
    processed: { color: 'bg-green-500/20 text-green-400', label: 'Ready', icon: CheckCircle },
    failed: { color: 'bg-red-500/20 text-red-400', label: 'Failed', icon: AlertCircle },
  };

  const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.uploaded;
  const Icon = config.icon;

  return (
    <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
      <Icon size={12} className="mr-1" />
      {config.label}
    </div>
  );
}