#include "Hexreader_Functions.hh"
#include "hexreader.hh"

namespace Hexreader__Functions {

	BOOLEAN f__readFile(const CHARSTRING& pl__path) {
		const char *src_ptr = pl__path;
		BOOLEAN ret_val(f_readFile(src_ptr));
		return ret_val;
	}

	BOOLEAN f__hasLine() {
		BOOLEAN ret_val(f_hasLine());
		return ret_val;
	}

	CHARSTRING f__readLine() {
		CHARSTRING ret_val(f_readLine());
		return ret_val;
	}

	BOOLEAN f__closeFile() {
		BOOLEAN ret_val(f_closeFile());
		return ret_val;
	}
}
