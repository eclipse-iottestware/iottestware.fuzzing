#include "Syscall_Functions.hh"
#include "syscall.hh"
#include <string>

namespace Syscall__Functions {

	CHARSTRING f__sysCall(const CHARSTRING& pl__call) {
		const char *src_ptr = pl__call;
		CHARSTRING ret_val(f_syscall(src_ptr));
		return ret_val;
	}
}
