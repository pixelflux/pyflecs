/* Copyright (c) 2022 Pixel Flux
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#pragma once

#include "flecs.h"
#include "entity.hpp"
#include "iter.hpp"
#include "filter.hpp"


namespace pyflecs {

    class query final {
    public:
        query(ecs_world_t* world, ecs_query_t* query);
        pyflecs::iter iter();

        int32_t term_count() const
        {
            return filter()->term_count;
        }

        const ecs_term_t& terms(size_t idx) const
        {
            auto f = filter();
            assert(idx < f->term_count);
            return f->terms[idx];
        }

    private:
        const ecs_filter_t* filter() const
        {
            return ecs_query_get_filter(mpRaw);
        }

        ecs_world_t* mpWorld;
        ecs_query_t* mpRaw;
    };
}